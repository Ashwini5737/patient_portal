from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
from chat import chat_bp
from views import views_bp
from appointment import appointment_bp


app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes
app.config["SECRET_KEY"] = "4b8e12f5a6d3c7e4a9b10d2e7f8a3c5d6e9f7b1a0c4d2e8f6a7b9c3d1e5f0a2"
app.config["SESSION_TYPE"] = "filesystem"  # Other options: 'redis', 'memcached', etc.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "myapp_"
app.config["SESSION_COOKIE_NAME"] = "my_flask_session"
print(app.config["SESSION_COOKIE_NAME"])
Session(app)

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(views_bp)
app.register_blueprint(appointment_bp,url_prefix='/appointment')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Use host='0.0.0.0' to make the server available on all your network adapters

