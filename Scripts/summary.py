import configparser
import openai

def get_config(section):
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    return {key: value for key, value in config.items(section)}
config = get_config('openai')
openai.api_key = config['api_key']
def generate_patient_summary(patient_data):
    """
    Generate a summary of the patient's recent medical records using OpenAI's GPT-4 model.
    """
    prompt = f"Please summarize the recent medical records for this patient data: Last Visit: {patient_data['LastVisitDate']}, Recent Medications: {patient_data['RecentMedications']}, Allergies: {patient_data['Allergies']}, Latest Encounter: {patient_data['LatestEncounterDescription']}, Immunizations: {patient_data['LatestImmunizations']}."
    completion = openai.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a medical assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content