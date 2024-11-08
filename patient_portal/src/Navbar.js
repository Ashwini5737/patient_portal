import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './Navbar.css';

const NavBar = () => {
    const navigate = useNavigate();
    const { id } = useParams(); // Fetching id directly inside NavBar

    console.log("NavBar ID:", id) 

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <nav>
            <button onClick={() => handleNavigation(`/patient/${id}`)}>Home</button>
            <button onClick={() => handleNavigation(`/appointment/${id}`)}>Appointment Booking</button>
            <button onClick={() => handleNavigation(`/dashboard/${id}`)}>Dashboard</button>
            <button onClick={() => handleNavigation(`/chat/${id}`)}>Chatbot</button>
            <button onClick={() => handleNavigation('/emergency')}>Emergency</button>
            <button onClick={() => navigate('/')}>Logout</button>
        </nav>
    );
};

export default NavBar;