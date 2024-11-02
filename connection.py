from flask import Flask, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
import pyodbc
import bcrypt

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

server = 'rjfenfxn7cyubgpcl5vvbiqcka-unveun7bepve5kpe2mbpwveqqu.datawarehouse.fabric.microsoft.com'
database = 'hackathon_data'
username = 'bhushanm@buffalo.edu'
auth = 'ActiveDirectoryInteractive'

connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};' \
                    f'SERVER={server};' \
                    f'DATABASE={database};' \
                    f'UID={username};' \
                    f'Authentication={auth};' \
                    f'ENCRYPT=yes;TrustServerCertificate=no;'

def get_db_connection():
    return pyodbc.connect(connection_string, timeout=10)

@app.route('/login', methods=['POST'])
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

@app.route('/login', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

if __name__ == '__main__':
    app.run(debug=True)
