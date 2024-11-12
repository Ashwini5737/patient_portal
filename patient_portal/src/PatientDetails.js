import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
// import PowerBIDashboard from './PowerBIDashboard';
import './PatientDetails.css';

function PatientDetails() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [patientDetails, setPatientDetails] = useState(null);
    const [summary, setSummary] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [viewMode, setViewMode] = useState('summary');

    useEffect(() => {
        const fetchPatientData = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5001/patient_data/${id}`);
                setPatientDetails(response.data.Details);
                setSummary(response.data.summary);
                setIsLoading(false);
            } catch (err) {
                console.error('Error fetching patient data:', err);
                setError('Failed to fetch patient data');
                setIsLoading(false);
            }
        };

        fetchPatientData();
    }, [id]);

    const handleChatClick = () => {
        navigate(`/chat/${id}`);
    };
    const handleDashboardClick = () => {
        navigate(`/dashboard/${id}`);  // This navigates to the dashboard page
    };
    
    const renderTableDetails = () => (
        <table>
            <tbody>
                {Object.entries(patientDetails).map(([key, value]) => (
                    <tr key={key}>
                        <td>{key}</td>
                        <td>{JSON.stringify(value, null, 2)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );

    return (
      <div className="patient-details-container">
          <div className="profile-summary">
              <div className="image-container">
                  <img src="/images/patient.jpeg" alt="Profile" />
              </div>
              <div className="summary-container">
                  {isLoading ? <p>Loading...</p> : error ? <p>{error}</p> : <p>{summary || 'No summary available'}</p>}
              </div>
          </div>
          <div className="view-toggle">
              <button onClick={() => setViewMode('summary')}>Summary</button>
              <button onClick={() => setViewMode('table')}>Table View</button>
          </div>
          <div className="details-view">
              {viewMode === 'table' && patientDetails ? renderTableDetails() : null}
          </div>
          <div className="dashboard-chatbot-container">
          <div className="dashboard-container" onClick={handleDashboardClick}>
                <h4>Detailed Patient Analytics</h4>
                <p>Explore comprehensive visual reports on patient health trends, treatment effectiveness, and more.</p>
          </div>
          <div className="chatbot-container" onClick={handleChatClick}>
                <h4>Interactive Patient Assistance</h4>
                <p>Have questions? Chat now with our intelligent assistant for guidance on health queries, medication details, and more.</p>
          </div>
        </div>

      </div>
  );
}

export default PatientDetails;
