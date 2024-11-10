import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const AppointmentBooking = () => {
    const { id } = useParams();
    const [filters, setFilters] = useState({
        state: '',
        city: '',
        zip: '',
        county: '',
        type: '',
        ownership: '',
        emergency: '',
        rating: ''
    });
    const [hospitals, setHospitals] = useState([]);
    const [error, setError] = useState('');
    const [filterOptions, setFilterOptions] = useState({
        states: [],
        cities: [],
        counties: [],
        types: [],
        ownerships: [],
        emergencies: []
    });

    const handleChange = (e) => {
        setFilters({ ...filters, [e.target.name]: e.target.value });
    };

    const fetchHospitals = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5001/appointment/${id}`, { params: filters });
            setHospitals(response.data);
            setError('');
        } catch (error) {
            setError('Failed to fetch hospitals: ' + error.message);
            console.error('Failed to fetch hospitals', error);
        }
    };

    const fetchFilterOptions = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5001/appointment/${id}?fetch_filters=true`);
            if (response.data) {
                setFilterOptions(response.data);
            }
        } catch (error) {
            setError('Failed to fetch filter options: ' + error.message);
            console.error('Failed to fetch filter options', error);
        }
    };

    useEffect(() => {
        fetchFilterOptions();
        fetchHospitals();
    }, [id]); // Only run on component mount

    return (
        <div>
            <h2>Appointment Booking</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
                <input name="state" value={filters.state} onChange={handleChange} placeholder="State" />
                <input name="city" value={filters.city} onChange={handleChange} placeholder="City/Town" />
                <input name="zip" value={filters.zip} onChange={handleChange} placeholder="ZIP Code" />
                <input name="county" value={filters.county} onChange={handleChange} placeholder="County" />
                <select name="type" value={filters.type} onChange={handleChange}>
                    <option value="">Select Hospital Type</option>
                    {filterOptions.types.map(type => (
                        <option key={type} value={type}>{type}</option>
                    ))}
                </select>
                <select name="ownership" value={filters.ownership} onChange={handleChange}>
                    <option value="">Select Hospital Ownership</option>
                    {filterOptions.ownerships.map(ownership => (
                        <option key={ownership} value={ownership}>{ownership}</option>
                    ))}
                </select>
                <select name="emergency" value={filters.emergency} onChange={handleChange}>
                    <option value="">Select Emergency Service</option>
                    {filterOptions.emergencies.map(emergency => (
                        <option key={emergency} value={emergency}>{emergency}</option>
                    ))}
                </select>
                <input name="rating" value={filters.rating} onChange={handleChange} placeholder="Overall Rating" />
                <button style={{ gridColumn: 'span 4' }} onClick={fetchHospitals}>Search Hospitals</button>
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <ul>
                {hospitals.map(hospital => (
                    <li key={hospital['Facility_ID']}>
                        <strong>{hospital['Facility_Name']}</strong> - {hospital['Address']}, {hospital['City_Town']}, {hospital['State']}
                        <br />Tel: {hospital['Telephone_Number']}
                        <br />Type: {hospital['Hospital_Type']} | Ownership: {hospital['Hospital_Ownership']} | Emergency: {hospital['Emergency_Services']}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AppointmentBooking;
