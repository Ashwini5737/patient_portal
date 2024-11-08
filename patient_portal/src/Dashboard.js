import React from 'react';

function Dashboard() {
    return (
        <div style={{ width: '100vw', height: '100vh', overflow: 'hidden' }}>
            <iframe
                title="Prajakta_dashboards"
                src="https://app.fabric.microsoft.com/reportEmbed?reportId=601ba9cc-b9de-48a8-8aed-10ce5b89d365&autoAuth=true&ctid=96464a8a-f8ed-40b1-99e2-5f6b50a20250"
                frameBorder="0"
                allowFullScreen={true}
                style={{ width: '100%', height: '100%' }}
            ></iframe>
        </div>
    );
}

export default Dashboard;
