// NavBar.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css'; // Make sure this path is correct based on your project structure

const NavBar = () => {
    const navigate = useNavigate();

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <nav>
            <button onClick={() => handleNavigation('/')}>Home</button>
            <button onClick={() => handleNavigation('/appointment')}>Appointment Booking</button>
            <button onClick={() => handleNavigation('/dashboard')}>Dashboard</button>
            <button onClick={() => handleNavigation('/chatbot')}>Chatbot</button>
            <button onClick={() => handleNavigation('/emergency')}>Emergency</button>
            <button onClick={() => handleNavigation('/login')}>Login</button>
        </nav>
    );
};

export default NavBar;
