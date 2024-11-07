// NavBar.js
import React from 'react';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './Navbar.css'; 

const NavBar = ({ patientId }) => {
    const { id } = useParams();
    const navigate = useNavigate();

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <nav>
            <button onClick={() => handleNavigation('/patient/${id}')}>Home</button>
            <button onClick={() => handleNavigation(`/apppointment/${id}`)}>Appointment Booking</button>
            <button onClick={() => handleNavigation(`/dashboard/${id}`)}>Dashboard</button>
            <button onClick={() => handleNavigation(`/chat/${id}`)}>Chatbot</button>
            <button onClick={() => handleNavigation('/emergency')}>Emergency</button>
            <button onClick={() => handleNavigation('/')}>Login</button>
        </nav>
    );
};

export default NavBar;
