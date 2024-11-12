from flask import Flask
from flask_session import Session
from flask_cors import CORS
from chat import chat_bp
from views import views_bp
from appointment import appointment_bp
app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(views_bp)
app.register_blueprint(appointment_bp,url_prefix='/appointment')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Use host='0.0.0.0' to make the server available on all your network adapters

