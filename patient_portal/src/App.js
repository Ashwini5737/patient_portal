import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import PatientDetails from './PatientDetails';
import ChatBot from './ChatBot';
import NavBar from './Navbar';
import AppointmentBooking from './AppointmentBooking'; // Make sure this file exists
import Dashboard from './Dashboard'; // Make sure this file exists
import Emergency from './Emergency'; // Make sure this file exists

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/patient/:id" element={<><NavBar /><PatientDetails /></>} />
        <Route path="/chat/:id" element={<><NavBar /><ChatBot /></>} />
        <Route path="/appointment/:id" element={<><NavBar /><AppointmentBooking /></>} />
        <Route path="/dashboard/:id" element={<><NavBar /><Dashboard /></>} />
        <Route path="/emergency" element={<Emergency />} />
      </Routes>
    </Router>
  );
};

export default App;