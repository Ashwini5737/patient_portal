from flask import Blueprint, request, jsonify
import openai
from db import get_db_connection
from flask_cors import CORS
from flask import current_app
import configparser
import openai

def get_config(section):
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    return {key: value for key, value in config.items(section)}

config = get_config('openai')
chat_bp = Blueprint('chat', __name__)
CORS(chat_bp, resources={r"/chat/*": {"origins": "*", "methods": ["POST", "OPTIONS"]}})
openai.api_key = config['api_key']

patient_context_cache = {}  # Simple in-memory cache
def fetch_patient_data(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = {}

    # Adjust the query to use cursor
    try:
        # Fetch allergies
        cursor.execute(
            'SELECT START, STOP, SYSTEM, DESCRIPTION, CATEGORY, REACTION1, DESCRIPTION1, SEVERITY1, REACTION2, DESCRIPTION2, SEVERITY2 FROM allergies WHERE PATIENT = ?', 
            (patient_id,)
        )
        allergies = cursor.fetchall()
        data['allergies'] = [dict(zip([column[0] for column in cursor.description], allergy)) for allergy in allergies]

        #Fetch Condition
        cursor.execute(
            'SELECT START, STOP, DESCRIPTION FROM conditions WHERE PATIENT = ?', 
            (patient_id,)
        )
        conditions = cursor.fetchall()
        data['conditions'] = [dict(zip([column[0] for column in cursor.description], condition)) for condition in conditions]

        #Fetch Encounters
        cursor.execute(
            'SELECT START, STOP, DESCRIPTION FROM encounters WHERE PATIENT = ?', 
            (patient_id,)
        )
        encounters = cursor.fetchall()
        data['encounters'] = [dict(zip([column[0] for column in cursor.description], encounter)) for encounter in encounters]

        #Fetch imaging studies
        cursor.execute(
            'SELECT DATE, BODYSITE_DESCRIPTION, MODALITY_DESCRIPTION, SOP_DESCRIPTION FROM imaging_studies WHERE PATIENT = ?', 
            (patient_id,)
        )
        imaging_studies = cursor.fetchall()
        data['imaging studies'] = [dict(zip([column[0] for column in cursor.description], imaging_studie)) for imaging_studie in imaging_studies]

        #Fetch Immunizations
        cursor.execute(
            'SELECT DATE , DESCRIPTION FROM immunizations WHERE PATIENT = ?', 
            (patient_id,)
        )
        immunizations = cursor.fetchall()
        data['immunizations'] = [dict(zip([column[0] for column in cursor.description], immunization)) for immunization in immunizations]
        
        #Fetch Medications
        cursor.execute(
            'SELECT START, STOP, DESCRIPTION, REASONDESCRIPTION FROM medications WHERE PATIENT = ?', 
            (patient_id,)
        )
        medications = cursor.fetchall()
        data['medications'] = [dict(zip([column[0] for column in cursor.description], medication)) for medication in medications]
        
        # Fetch observations
        cursor.execute(
            'SELECT DATE, DESCRIPTION,CATEGORY, TYPE FROM observations WHERE PATIENT = ?', 
            (patient_id,)
        )
        observations = cursor.fetchall()
        data['observations'] = [dict(zip([column[0] for column in cursor.description], observation)) for observation in observations]
        
        #Fetch name
        cursor.execute(
        'SELECT FIRST, LAST FROM patients WHERE Id = ?', 
        (patient_id,))

        patient_info = cursor.fetchone()
        data['name'] = f"{patient_info[0]} {patient_info[1]}" if patient_info else "Unnamed Patient"
    except Exception as e:
        print(f"Error fetching patient data: {str(e)}")  # Log the error for debugging
        data = {}  # Reset data on failure
    finally:
        cursor.close()
        conn.close()

    return data

def create_prompt(patient_id, patient_data):
    patient_name = patient_data.pop('name', 'Unnamed Patient')
    context_parts = [f"Patient ID {patient_id}, {patient_name}, has the following medical record:"]
    for category, entries in patient_data.items():
        context_parts.append(f"{category.upper()}:")
        for entry in entries:
            entry_desc = ', '.join([f"{key}={value}" for key, value in entry.items() if value])
            context_parts.append(entry_desc)
    
    context = " ".join(context_parts)
    system_role = "As a medical assistant, you need to consider the following data to provide the best advice:"
    prompt = f"{system_role} {context}"
    return prompt

@chat_bp.route('/<patient_id>', methods=['POST'])
def chat(patient_id):
    print("Patient ID:", patient_id)
    user_message = request.json.get('message')
    patient_data = fetch_patient_data(patient_id)
    if not patient_data:
        return jsonify({'error': 'Failed to fetch patient data'}), 500

    prompt = create_prompt(patient_id, patient_data)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150
        )
        assistant_message = response.choices[0].message.content.strip() if response.choices else "No response from the model."
    except Exception as e:
        current_app.logger.error(f"Error communicating with OpenAI: {str(e)}")
        assistant_message = "Error communicating with the chatbot."

    return jsonify({'response': assistant_message})

