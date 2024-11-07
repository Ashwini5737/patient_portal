import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';  // Assuming you have a CSS file for styling

function Login() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5001/login', {
        first: firstName,
        last: lastName,
        password: password
      });
      navigate(`/patient/${response.data.patient_id}`); // Redirect on successful login
    } catch (error) {
      alert(error.response ? error.response.data.message : 'Server error');
    }
  };

  return (
    <div className="login-container">
      <h2>PatientPortal Login</h2>
      <form onSubmit={handleLogin} className="login-form">
        <input type="text" value={firstName} placeholder="First Name" onChange={e => setFirstName(e.target.value)} />
        <input type="text" value={lastName} placeholder="Last Name" onChange={e => setLastName(e.target.value)} />
        <input type="password" value={password} placeholder="Password" onChange={e => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
