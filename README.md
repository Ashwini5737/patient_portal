# Patient Portal

A Flask-based patient portal application providing patients with an overview of their medical records, hospital search functionality, personalized chatbot assistance, Power BI visualizations, and an emergency contact interface. The portal leverages Microsoft Fabric and OpenAI for secure data management and contextual assistance. Below is the workflow of our patient portal.

![image](https://github.com/user-attachments/assets/72869bfe-3d6e-4201-a191-ce8a9b12e5ea)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Directory Structure](#directory-structure)
- [Troubleshooting](#troubleshooting)

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
- 
## Data Setup and Backend Preparation

To run this application, follow the steps below to set up data and configure the backend:

1. **Data Extraction**:
   - Use the **Synthea API** to generate synthetic patient data. This will create CSV files for 18 different tables related to patient data (e.g., `patients`, `medications`, `allergies`, etc.).
   
2. **Data Upload to Microsoft Fabric**:
   - Upload each CSV file to **Microsoft Fabric** as tables using the "Load into Tables" feature.
   - Create a **semantic model** within Microsoft Fabric, using SQL Endpoints to connect and relate tables logically, enabling structured queries on patient data.

3. **SQL Endpoint Testing**:
   - Use SQL queries within Microsoft Fabric to test your semantic model and ensure relationships among tables are correctly defined.
   - Retrieve the **connection string** for your SQL Endpoint, which will be used to connect to your database from the backend.

4. **Hospital Database Setup**:
   - Similarly, a **hospital database** (for locating hospitals based on patient location), add this data to Microsoft Fabric.
   - **Hospital Data Preprocessing:**
     For the hospital data, use a notebook within Microsoft Fabric and run the following PySpark code to clean and preprocess the hospital data into 12 essential columns. This code reads the hospital data CSV file, selects specific columns, removes any rows with missing values in these columns, cleans the column names, and saves the cleaned data as a new CSV file.

      ```python
      from pyspark.sql import SparkSession
      
      spark = SparkSession.builder \
          .appName("Hospital Data Cleaning") \
          .getOrCreate()
      file_path = "Files/Hospital_General_Information.csv"  # Update this to the path of your data file
      df = spark.read.format("csv").option("header", "true").load(file_path)
      columns_to_keep = [
          "Facility ID", "Facility Name", "Address", "City/Town", "State",
          "ZIP Code", "County/Parish", "Telephone Number", "Hospital Type", 
          "Hospital Ownership", "Emergency Services", "Hospital overall rating"
      ]
      cleaned_df = df.select(*columns_to_keep).dropna(how="any", subset=columns_to_keep)
      def clean_column_names(df):
          for col in df.columns:
              new_col = col.strip().replace(" ", "_").replace("/", "_").replace("-", "_")
              df = df.withColumnRenamed(col, new_col)
          return df
      cleaned_df_1 = clean_column_names(cleaned_df)
      output_path = "Files/Cleaned_hospital_data"  # Update this to your desired output path
      cleaned_df_1.coalesce(1).write.format("csv").option("header", "true").save(output_path)
      ```

5. **Configuration in Backend Code**:
   - Add the SQL Endpoint connection string into the `db_config.ini` file within your project. Include your **username** and **password** for secure connection management.
   - Obtain an **OpenAI API key** and include it in the `db_config.ini` file for chatbot and summary generation functionality.

After completing these steps, your backend should be able to access the patient data and hospital data stored in Microsoft Fabric, enabling the application to perform data retrieval and analysis effectively.


## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Bhushan4829/microsoft_fabric_hackathon.git
   ```
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Setup:** Ensure that your database connection configurations (e.g., db_config.ini) are properly set with the necessary credentials for Microsoft Fabric and SQL endpoints.

## Configuration
1. **Sensitive Data:** Ensure sensitive data like API keys and database credentials are kept in db_config.ini and are not exposed. The config file should include:
   ```ini
   [openai]
   api_key = your_openai_api_key

   [database]
   driver=ODBC Driver 18 for SQL Server
   server= Your Connection String
   database=Your Database
   uid=Your Microsoft Account email id
   password= Your Microsoft Account Password

   [hospital_database]
   driver=ODBC Driver 18 for SQL Server
   server= Your Connection String
   database=Your Database
   uid=Your Microsoft Account email id
   password= Your Microsoft Account Password
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
