# Patient Portal

A Flask-based patient portal application providing patients with an overview of their medical records, hospital search functionality, personalized chatbot assistance, Power BI visualizations, and an emergency contact interface. The portal leverages Microsoft Fabric and OpenAI for secure data management and contextual assistance.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Directory Structure](#directory-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Patient Dashboard**: Displays recent medical data, including last visit, encounter description, prescribed medications, immunizations, allergies, and imaging studies. The dashboard also features a profile photo (to be updated by users in future versions).
- **Hospital Locator**: Search for hospitals based on various filters like location, type, and services.
- **Power BI Dashboard**: Visualize patient data with Microsoft Fabric Power BI.
- **Chatbot**: An AI-powered chatbot with patient-specific data for personalized interaction and insights.
- **Emergency Contacts**: A dedicated section for quick access to important emergency contacts.

## Tech Stack

- **Backend**: Python, Flask, Microsoft Fabric (Lakehouse for data storage)
- **Database**: SQL Endpoints via Microsoft Fabric for querying
- **Frontend**: JavaScript, React.js, CSS
- **AI**: OpenAI API for chatbot and patient summaries
- **Other**: Flask-CORS, Flask-Session for session management, bcrypt for password hashing

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Bhushan4829/microsoft_fabric_hackathon.git
   ```
2. Set up a virtual environment(Optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Database Setup:** Ensure that your database connection configurations (e.g., db_config.ini) are properly set with the necessary credentials for Microsoft Fabric and SQL endpoints.

## Configuration
1. **Sensitive Data:** Ensure sensitive data like API keys and database credentials are kept in db_config.ini and are not exposed. The config file should include:
   ```ini
   [openai]
   api_key = your_openai_api_key

   [database]
   connection_string = your_database_connection_string
   ```
2. **Session and CORS Configuration:**
   - The app uses Flask-Session to manage user sessions and Flask-CORS for cross-origin requests. If needed, modify the settings in app.py.
3. **Azure Authentication:** If you are using Azure Interactive Browser Credential for authentication, configure the SCP scope and other details in views.py.

## Usage
1. **Run the Backend Application:**
   ```bash
   python app.py
   ```
   Access the app at http://127.0.0.1:5001.
2. **Run Frontend Application:**
   ```bash
   cd patient_portal
   npm install
   npm start
   ```
4. API Documentation

- **Login**: `POST /login` - Authenticate the user.
- **Signup**: `POST /signup` - Register a new patient account.
- **Logout**: `GET /logout` - End the session.
- **Fetch Patient Data**: `GET /patient_data/<patient_id>` - Retrieve recent medical data for a specific patient.
- **Chatbot**: `POST /chat/<patient_id>` - Submit a user message for AI-powered responses based on the patient's data.
- **Book Appointment**: `GET /appointment/<patient_id>` - Search for nearby hospitals based on filters such as state, city, and zip code.
- **Front-End Access**: The front end is implemented with React.js; you may need to set up a separate front-end server if it is hosted independently from the Flask backend.

## API Endpoints

### Authentication

- **Login**: `POST /login` — Authenticate the user.
- **Signup**: `POST /signup` — Register a new patient account.
- **Logout**: `GET /logout` — End the session.

### Patient Data Retrieval

- **Patient Data**: `GET /patient_data/<patient_id>` — Fetch recent medical data for a specific patient.
- **Chatbot**: `POST /chat/<patient_id>` — Submit a user message for AI-powered responses based on the patient's data.

### Appointments

- **Hospital Search and Filter**: `GET /appointment/<patient_id>` — Search for nearby hospitals based on various filters, including state, city, and zip code.

### Power BI Integration

Integrates with Microsoft Fabric to generate a Power BI dashboard using patient data, accessible via a specific navigation link on the homepage.

## Directory Structure

```plaintext
microsoft_fabric_hackathon/
├── patient_portal/
│   ├── App.js
│   ├── App.css
│   ├── AppointmentBooking.js
│   ├── AppointmentBooking.css
│   ├── ChatBot.js
│   ├── ChatBot.css
│   ├── Dashboard.js
│   ├── Login.js
│   ├── Login.css
│   ├── Navbar.js
│   ├── Navbar.css
│   ├── PatientDetails.js
│   ├── PatientDetails.css
│   ├── Signup.js
│   ├── Signup.css
├── scripts/
│   ├── views.py         # API routes for login, signup, and patient data
│   ├── chat.py          # Chatbot functionality and patient data fetch
│   ├── summary.py       # Patient summary generator using OpenAI
│   ├── appointment.py   # Appointment and hospital locator
│   ├── app.py           # Main application entry point
│   ├── db_config.ini    # Configuration file for database credentials (not in version control)        
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation
```

## Troubleshooting
- Database Connection Issues: Ensure db_config.ini is correctly configured and that your database is reachable.
- Azure Authentication: Verify the scope and permissions required for Azure.
- OpenAI Errors: Ensure your OpenAI API key is valid and has access to required models.
