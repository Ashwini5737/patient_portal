import React from 'react';
import { Link } from 'react-router-dom'; // if you need to link to other routes
import './Emergency.css'
const Emergency = () => {
    return (
        <div className="emergency-container">
            <h1>Emergency Contacts & Information</h1>
            <div className="emergency-contacts">
                <h2>Contact Numbers</h2>
                <p>Local Police: 911</p>
                <p>Fire Department: 911</p>
                <p>Ambulance: 911</p>
                <p>Poison Control: 1-800-222-1222</p>
            </div>
            <div className="first-aid-info">
                <h2>First Aid Tips</h2>
                <Link to="https://www.youtube.com/watch?v=gn6xt1ca8A0&t=2s">Learn Basic First Aid</Link>
            </div>
        </div>
    );
}

export default Emergency;
