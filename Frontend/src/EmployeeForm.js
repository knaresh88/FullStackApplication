// EmployeeForm.js
import React, { useState } from 'react';
import axios from 'axios';

const EmployeeForm = ({ onEmployeeAdded, setEmployees }) => {
  const [formData, setFormData] = useState({
    name: '',
    birthdate: '',
    department: '',
    salary: '',
  });

  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');


  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8002/api/emp/', formData);
      console.log('Response from server:', response.data);
      setSuccessMessage('Employee added successfully.');
      setErrorMessage('');

      // Call onEmployeeAdded function with the new employee data
      onEmployeeAdded(response.data);

      setFormData({
        name: '',
        birthdate: '',
        department: '',
        salary: '',
      });

      // Update employees state using the callback function (if provided)
      if (setEmployees) {
        setEmployees(prevEmployees => [...prevEmployees, response.data]);
      }

    } catch (error) {
      console.error('Error adding employee:', error.response || error);
      setErrorMessage('Failed to add employee. Please try again.');
      setSuccessMessage('');
    }
  };

  


  return (
    <div>
      <h2>Add Employee</h2>
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} autoComplete="name"/>
        <input type="date" name="birthdate" value={formData.birthdate} onChange={handleChange} autoComplete="bday"/>
        <input type="text" name="department" placeholder="Department" value={formData.department} onChange={handleChange} autoComplete="organization"/>
        <input type="number" name="salary" placeholder="Salary" value={formData.salary} onChange={handleChange} autoComplete="salary"/>
        <button type="submit">Add Employee</button>
      </form>
    </div>
  );
};

export default EmployeeForm;
