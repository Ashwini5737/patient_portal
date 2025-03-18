import React from 'react';
import './PowerBIDashboard.css';

const PowerBIDashboard = () => {
    const dashboardUrl = process.env.REACT_APP_DASHBOARD_URL;
    const dashboardName = process.env.REACT_APP_DASHBOARD_NAME;
    return (
        <div className="powerbi-dashboard">
            <iframe
                title={dashboardName}
                width="1140"
                height="541.25"
                src={dashboardUrl}
                frameBorder="0"
                allowFullScreen="true"
                style={{ border: 'none' }} // Optional: Add style to remove border
            ></iframe>
        </div>
    );
};

export default PowerBIDashboard;
