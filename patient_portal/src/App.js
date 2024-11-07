import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import PatientDetails from './PatientDetails';
import ChatBot from './ChatBot';  // Import the ChatBot component
import NavBar from './Navbar';

function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/patient/:id" element={<PatientDetails />} />
        <Route path="/chat/:id" element={<ChatBot />} />
      </Routes>
    </Router>
  );
}

export default App;