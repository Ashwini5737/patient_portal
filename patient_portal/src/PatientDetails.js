import React from 'react';
import { useParams } from 'react-router-dom';

function PatientDetails() {
  const { id } = useParams(); // Get patient ID from URL

  return (
    <div>
      <h1>Patient Details</h1>
      <p>Patient ID: {id}</p>
      {/* Additional patient details can be fetched and displayed here */}
    </div>
  );
}

export default PatientDetails;
