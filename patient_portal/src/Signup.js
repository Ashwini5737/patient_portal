import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Signup.css';  // Assuming you have a CSS file for styling

function Signup() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [birthdate, setBirthdate] = useState('');
  const [ssn, setSSN] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5001/signup', {
        first: firstName,
        last: lastName,
        birthdate: birthdate,
        ssn: ssn,
        password: password
      });
      console.log(response.data);
      navigate(`/patient/${response.data.patient_id}`); // Redirect on successful signup
      
    } catch (error) {
      alert(error.response ? error.response.data.message : 'Server error');
    }
  };

  return (
    <div className="signup-container">
      <h2>PatientPortal Signup</h2>
      <form onSubmit={handleSignup} className="signup-form">
        <input type="text" value={firstName} placeholder="First Name" onChange={e => setFirstName(e.target.value)} />
        <input type="text" value={lastName} placeholder="Last Name" onChange={e => setLastName(e.target.value)} />
        <input type="date" value={birthdate} placeholder="Birthdate" onChange={e => setBirthdate(e.target.value)} />
        <input type="text" value={ssn} placeholder="SSN" onChange={e => setSSN(e.target.value)} />
        <input type="password" value={password} placeholder="Password" onChange={e => setPassword(e.target.value)} />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;

