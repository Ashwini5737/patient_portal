import React from 'react';
import './PowerBIDashboard.css';

const PowerBIDashboard = () => {
    return (
        <div className="powerbi-dashboard">
            <iframe
                title="Prajakta_dashboards"
                width="1140"
                height="541.25"
                src="https://app.powerbi.com/reportEmbed?reportId=601ba9cc-b9de-48a8-8aed-10ce5b89d365&autoAuth=true&ctid=96464a8a-f8ed-40b1-99e2-5f6b50a20250"
                frameBorder="0"
                allowFullScreen="true"
                style={{ border: 'none' }} // Optional: Add style to remove border
            ></iframe>
        </div>
    );
};

export default PowerBIDashboard;
