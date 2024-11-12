import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './Navbar.css';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faCalendarAlt, faTachometerAlt, faComments, faExclamationTriangle, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

const NavBar = () => {
    const navigate = useNavigate();
    const { id } = useParams();

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <nav>
            <button onClick={() => handleNavigation(`/patient/${id}`)}><FontAwesomeIcon icon={faHome} /> Home</button>
            <button onClick={() => handleNavigation(`/appointment/${id}`)}><FontAwesomeIcon icon={faCalendarAlt} /> Locate Hospital</button>
            <button onClick={() => handleNavigation(`/dashboard/${id}`)}><FontAwesomeIcon icon={faTachometerAlt} /> Dashboard</button>
            <button onClick={() => handleNavigation(`/chat/${id}`)}><FontAwesomeIcon icon={faComments} /> Chatbot</button>
            <button onClick={() => handleNavigation('/emergency')}><FontAwesomeIcon icon={faExclamationTriangle} /> Emergency</button>
            <button onClick={() => navigate('/')}><FontAwesomeIcon icon={faSignOutAlt} /> Logout</button>
        </nav>
    );
};

export default NavBar;
