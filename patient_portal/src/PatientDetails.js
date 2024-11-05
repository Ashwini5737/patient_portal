import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import PowerBIDashboard from './PowerBIDashboard';
import ChatBot from './ChatBot';
import './PatientDetails.css';

function PatientDetails() {
    const { id } = useParams();
    const [patientDetails, setPatientDetails] = useState(null);
    const [summary, setSummary] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/patient_data/${id}`)
            .then(response => {
                setPatientDetails(response.data.Details);
                setSummary(response.data.summary);
                setIsLoading(false);
            })
            .catch(err => {
                console.error('Error fetching patient data:', err);
                setError('Failed to fetch patient data');
                setIsLoading(false);
            });
    }, [id]);

    return (
        <div className="patient-details-container">
            <div className="profile-summary">
                <div className="image-container">
                    <img src="/images/patient.jpeg" alt="Profile" />  {/* Update path as needed */}
                </div>
                <div className="summary-container">
                    {isLoading ? <p>Loading...</p> : error ? <p>{error}</p> : <p>{summary || 'No summary available'}</p>}
                </div>
            </div>
            <div className="dashboard-chatbot-container">
                <div className="dashboard-container">
                    <PowerBIDashboard />
                </div>
                <div className="chatbot-container">
                    <ChatBot patientData={patientDetails} />
                </div>
            </div>
        </div>
    );
}

export default PatientDetails;
