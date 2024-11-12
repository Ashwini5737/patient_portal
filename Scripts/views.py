from flask import Blueprint, request, session, jsonify
from db import get_db_connection  # Assuming you've abstracted database connection logic
import bcrypt
from summary import generate_patient_summary
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from flask import current_app
from bcrypt import hashpw, gensalt
from azure.identity import InteractiveBrowserCredential
views_bp = Blueprint('views', __name__)


def get_authenticated_transport():
    app = InteractiveBrowserCredential()
    scp = 'https://analysis.windows.net/powerbi/api/user_impersonation'
    result = app.get_token(scp)

    if not result.token:
        raise Exception("Could not get access token")

    transport = RequestsHTTPTransport(
        url='https://api.fabric.microsoft.com/v1/workspaces/374a6aa3-23e1-4eea-a9e4-d302fb549085/graphqlapis/f56b47e1-74c6-40ee-95e2-12d591459dec/graphql',
        use_json=True,
        verify=True,  # Depends on your server's SSL setup
        retries=3,
        headers={
            'Authorization': f'Bearer {result.token}',
            'Content-Type': 'application/json'
        }
    )
    return transport

@views_bp.route('/login', methods=['POST'])
def login():
    first_name = request.json['first']
    last_name = request.json['last']
    password = request.json['password'].encode('utf-8')

    cnxn = get_db_connection()
    cursor = cnxn.cursor()
    cursor.execute("SELECT Id, PASSWORD FROM patients_with_passwords WHERE FIRST = ? AND LAST = ?", (first_name, last_name))
    user = cursor.fetchone()
    cursor.close()
    cnxn.close()

    if user and bcrypt.checkpw(password, user.PASSWORD.encode('utf-8')):
        session['user_id'] = user.Id
        return jsonify({"message": "Login successful", "patient_id": user.Id}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
@views_bp.route('/signup', methods=['POST'])
def signup():
    first_name = request.json.get('first')
    last_name = request.json.get('last')
    birthdate = request.json.get('birthdate')
    ssn = request.json.get('ssn')
    password = request.json.get('password').encode('utf-8')
    hashed_password = hashpw(password, gensalt()).decode('utf-8')

    cnxn = get_db_connection()
    cursor = cnxn.cursor()

    try:
        # Check if the user already exists
        check_user_query = """
            SELECT Id FROM patients_with_passwords
            WHERE FIRST = ? AND LAST = ? AND SSN = ?
        """
        cursor.execute(check_user_query, (first_name, last_name, ssn))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"message": "User already exists"}), 409

        # Insert the new user record
        create_user_query = """
            INSERT INTO patients_with_passwords (FIRST, LAST, BIRTHDATE, SSN, PASSWORD)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(create_user_query, (first_name, last_name, birthdate, ssn, hashed_password))
        cnxn.commit()

        # Retrieve the ID of the newly created user
        user_id = cursor.lastrowid
        return jsonify({"message": "Signup successful", "patient_id": str(user_id)}), 200

    except Exception as e:
        current_app.logger.error('Error during signup: %s', str(e))
        return jsonify({"error": "Error during signup process"}), 500

    finally:
        cursor.close()
        cnxn.close()


@views_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

@views_bp.route('/patient_data/<patient_id>', methods=['GET'])
def get_patient_data(patient_id):
    try:
        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        query = "SELECT p.Id, COALESCE(le.LastVisitDate, 'No recent visit') AS LastVisitDate, COALESCE(lm.LatestMedication, 'No recent medications') AS RecentMedications, COALESCE(la.Allergies, 'No known allergies') AS Allergies, COALESCE(le.LatestEncounterDescription, 'No recent encounter') AS LatestEncounterDescription, COALESCE(li.LatestImmunizations, 'No immunizations recorded') AS LatestImmunizations, COALESCE(lim.BodySiteDescription, 'N/A') AS BodySiteDescription, COALESCE(lim.ModalityDescription, 'N/A') AS ModalityDescription, COALESCE(lim.SOPDescription, 'N/A') AS SOPDescription FROM patients p LEFT JOIN (SELECT e.PATIENT AS PATIENT_ID, e.DESCRIPTION AS LatestEncounterDescription, e.START AS LastVisitDate, ROW_NUMBER() OVER (PARTITION BY e.PATIENT ORDER BY e.START DESC) AS rn FROM encounters e WHERE e.DESCRIPTION IS NOT NULL) le ON p.Id = le.PATIENT_ID AND le.rn = 1 LEFT JOIN (SELECT m.PATIENT AS PATIENT_ID, m.DESCRIPTION AS LatestMedication, m.START AS MedicationStartDate, ROW_NUMBER() OVER (PARTITION BY m.PATIENT ORDER BY m.START DESC) AS rn FROM medications m WHERE m.DESCRIPTION IS NOT NULL) lm ON p.Id = lm.PATIENT_ID AND lm.rn = 1 LEFT JOIN (SELECT i.PATIENT AS PATIENT_ID, i.DESCRIPTION AS LatestImmunizations, i.DATE AS ImmunizationDate, ROW_NUMBER() OVER (PARTITION BY i.PATIENT ORDER BY i.DATE DESC) AS rn FROM immunizations i WHERE i.DESCRIPTION IS NOT NULL) li ON p.Id = li.PATIENT_ID AND li.rn = 1 LEFT JOIN (SELECT a.PATIENT AS PATIENT_ID, a.DESCRIPTION AS Allergies, a.START AS AllergyStartDate, ROW_NUMBER() OVER (PARTITION BY a.PATIENT ORDER BY a.START DESC) AS rn FROM allergies a WHERE a.DESCRIPTION IS NOT NULL) la ON p.Id = la.PATIENT_ID AND la.rn = 1 LEFT JOIN (SELECT isd.PATIENT AS PATIENT_ID, isd.BODYSITE_DESCRIPTION AS BodySiteDescription, isd.MODALITY_DESCRIPTION AS ModalityDescription, isd.SOP_DESCRIPTION AS SOPDescription, isd.DATE AS ImagingDate, ROW_NUMBER() OVER (PARTITION BY isd.PATIENT ORDER BY isd.DATE DESC) AS rn FROM imaging_studies isd WHERE isd.BODYSITE_DESCRIPTION IS NOT NULL) lim ON p.Id = lim.PATIENT_ID AND lim.rn = 1 WHERE p.Id = ?;"

        print("Executing SQL Query:", query)
        print("With patient ID:", patient_id)
        cursor.execute(query, (patient_id,))

        row = cursor.fetchone()
        
        if row:
            # Transform the row into a dictionary using column headers
            col_names = [desc[0] for desc in cursor.description]
            patient_data = dict(zip(col_names, row))
            summary = generate_patient_summary(patient_data)
            return jsonify({'summary': summary, 'Details': patient_data})
        else:
            return jsonify({'message': 'No patient data found'}), 404

    except Exception as e:
        views_bp.logger.error(f"Error fetching patient data: {str(e)}")
        return jsonify({"error": "Error fetching data"}), 500
    finally:
        cursor.close()
        cnxn.close()