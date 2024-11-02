import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import PatientDetails from './PatientDetails';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/patient/:id" element={<PatientDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

