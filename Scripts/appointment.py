from flask import Blueprint, request, jsonify  # Import your specific DB connection setup
from db import get_hospital_db_connection
from flask_cors import CORS
import traceback
appointment_bp = Blueprint('appointment', __name__)
CORS(appointment_bp, resources={r"/appointment/*": {"origins": "*", "methods": ["POST", "OPTIONS"]}})
@appointment_bp.route('/<patient_id>', methods=['GET'])
def book_appointment(patient_id):
    fetch_filters = request.args.get('fetch_filters', type=str)
    if fetch_filters:
        return fetch_filter_data()
    state = request.args.get('state', type=str)
    city = request.args.get('city', type=str)
    zip_code = request.args.get('zip', type=str)  # Renamed to avoid using `zip` which is a built-in Python function
    cnxn = get_hospital_db_connection()
    cursor = cnxn.cursor()

    params = request.args
    query = """
    SELECT TOP 10 [Facility_ID], [Facility_Name], [Address], [City_Town], [State], [ZIP_Code], [County_Parish], 
    [Telephone_Number], [Hospital_Type], [Hospital_Ownership], [Emergency_Services], [Hospital_overall_rating]
    FROM hospital
    WHERE 
        ([State] = ? OR ? = '') AND
        ([City_Town] = ? OR ? = '') AND
        ([ZIP_Code] = ? OR ? = '') AND
        ([County_Parish] = ? OR ? = '') AND
        ([Hospital_Type] = ? OR ? = '') AND
        ([Hospital_Ownership] = ? OR ? = '') AND
        ([Emergency_Services] = ? OR ? = '') AND
        ([Hospital_overall_rating] = ? OR ? = '')
    ORDER BY [Facility_Name] ASC
    """
    filters = [params.get('state', ''), params.get('state', ''),
               params.get('city', ''), params.get('city', ''),
               params.get('zip', ''), params.get('zip', ''),
               params.get('county', ''), params.get('county', ''),
               params.get('type', ''), params.get('type', ''),
               params.get('ownership', ''), params.get('ownership', ''),
               params.get('emergency', ''), params.get('emergency', ''),
               params.get('rating', ''), params.get('rating', '')]

    try: 
        cursor.execute(query, filters)
        hospitals = cursor.fetchall()
        hospital_data = [dict(zip([column[0] for column in cursor.description], hospital)) for hospital in hospitals]
        return jsonify(hospital_data), 200
    except Exception as e:
        print(f"Error fetching hospital data: {str(e)}")
        return jsonify({"error": "Error fetching data"}), 500
    finally:
        cursor.close()
        cnxn.close()
def fetch_filter_data():
    cnxn = get_hospital_db_connection()
    cursor = cnxn.cursor()
    try:
        # Example: Fetching unique states for the dropdown
        cursor.execute("SELECT DISTINCT [State] FROM hospital")
        states = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT [City_Town] FROM hospital")
        cities = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT [County_Parish] FROM hospital")
        counties = [row[0] for row in cursor.fetchall()]

        # Fetching unique hospital types
        cursor.execute("SELECT DISTINCT [Hospital_Type] FROM hospital")
        types = [row[0] for row in cursor.fetchall()]

        # Fetching unique hospital ownerships
        cursor.execute("SELECT DISTINCT [Hospital_Ownership] FROM hospital")
        ownerships = [row[0] for row in cursor.fetchall()]

        # Fetching unique emergency services
        cursor.execute("SELECT DISTINCT [Emergency_Services] FROM hospital")
        emergencies = [row[0] for row in cursor.fetchall()]

        # Fetching unique hospital ratings (if applicable)
        cursor.execute("SELECT DISTINCT [Hospital_overall_rating] FROM hospital")
        ratings = [row[0] for row in cursor.fetchall()]

        return jsonify({
            "states": states,
            "cities": cities,
            "counties": counties,
            "types": types,
            "ownerships": ownerships,
            "emergencies": emergencies,
            "ratings": ratings
        }), 200
    except Exception as e:
        print(f"Error fetching filter data: {str(e)}")
        return jsonify({"error": "Error fetching data"}), 500
    finally:
        cursor.close()
        cnxn.close()


# from flask import Blueprint, request, jsonify
# from db import get_hospital_db_connection  # Make sure to import your specific DB connection setup
# from flask_cors import CORS

# appointment_bp = Blueprint('appointment', __name__)
# CORS(appointment_bp, resources={r"/appointment/*": {"origins": "*", "methods": ["GET"]}})

# @appointment_bp.route('/<patient_id>', methods=['GET'])
# def book_appointment(patient_id):
#     fetch_filters = request.args.get('fetch_filters', type=bool)
#     filter_type = request.args.get('filter_type', type=str)
#     state = request.args.get('state', type=str)

#     if fetch_filters:
#         if filter_type == 'initial':
#             return fetch_initial_filters()
#         elif filter_type == 'city':
#             return fetch_cities(state)
#         elif filter_type == 'county':
#             return fetch_counties(state)
#         else:
#             return jsonify({"error": "Invalid filter type"}), 400

#     # Prepare to fetch hospital data based on filters
#     params = {
#         'state': request.args.get('state', default='', type=str),
#         'city': request.args.get('city', default='', type=str),
#         'zip': request.args.get('zip', default='', type=str),
#         'county': request.args.get('county', default='', type=str),
#         'type': request.args.get('type', default='', type=str),
#         'ownership': request.args.get('ownership', default='', type=str),
#         'emergency': request.args.get('emergency', default='', type=str),
#         'rating': request.args.get('rating', default='', type=str)
#     }
#     return fetch_hospitals(params)

# def fetch_hospitals(filters):
#     cnxn = get_hospital_db_connection()
#     cursor = cnxn.cursor()
#     query = """
#     SELECT TOP 10 [Facility_ID], [Facility_Name], [Address], [City_Town], [State], [ZIP_Code], [County_Parish],
#     [Telephone_Number], [Hospital_Type], [Hospital_Ownership], [Emergency_Services], [Hospital_overall_rating]
#     FROM hospital
#     WHERE 
#         (State = ? OR ? = '') AND
#         (City_Town = ? OR ? = '') AND
#         (ZIP_Code = ? OR ? = '') AND
#         (County_Parish = ? OR ? = '') AND
#         (Hospital_Type = ? OR ? = '') AND
#         (Hospital_Ownership = ? OR ? = '') AND
#         (Emergency_Services = ? OR ? = '') AND
#         (Hospital_overall_rating = ? OR ? = '')
#     ORDER BY [Facility_Name]
#     """
#     params = [filters[k] for k in ('state', 'state', 'city', 'city', 'zip', 'zip', 'county', 'county', 'type', 'type', 'ownership', 'ownership', 'emergency', 'emergency', 'rating', 'rating')]
#     cursor.execute(query, params)
#     result = cursor.fetchall()
#     hospitals = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
#     cursor.close()
#     cnxn.close()
#     return jsonify(hospitals)

# def fetch_cities(state):
#     cnxn = get_hospital_db_connection()
#     cursor = cnxn.cursor()
#     query = "SELECT DISTINCT City_Town FROM hospital WHERE State = ?"
#     cursor.execute(query, (state,))
#     cities = [row[0] for row in cursor.fetchall()]
#     cursor.close()
#     cnxn.close()
#     return jsonify({"cities": cities})

# def fetch_counties(state):
#     cnxn = get_hospital_db_connection()
#     cursor = cnxn.cursor()
#     query = "SELECT DISTINCT County_Parish FROM hospital WHERE State = ?"
#     cursor.execute(query, (state,))
#     counties = [row[0] for row in cursor.fetchall()]
#     cursor.close()
#     cnxn.close()
#     return jsonify({"counties": counties})

# def fetch_initial_filters():
#     cnxn = get_hospital_db_connection()
#     cursor = cnxn.cursor()
#     cursor.execute("SELECT DISTINCT State FROM hospital")
#     states = [row[0] for row in cursor.fetchall()]
#     cursor.execute("SELECT DISTINCT Hospital_Type FROM hospital")
#     types = [row[0] for row in cursor.fetchall()]
#     cursor.execute("SELECT DISTINCT Hospital_Ownership FROM hospital")
#     ownerships = [row[0] for row in cursor.fetchall()]
#     cursor.execute("SELECT DISTINCT Emergency_Services FROM hospital")
#     emergencies = [row[0] for row in cursor.fetchall()]
#     cursor.close()
#     cnxn.close()
#     filters_data = {
#         "states": states,
#         "types": types,
#         "ownerships": ownerships,
#         "emergencies": emergencies
#     }
#     print("Filters data being returned:", filters_data)  # Debug output
#     return jsonify(filters_data)
