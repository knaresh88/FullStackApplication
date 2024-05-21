// App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EmployeeForm from './EmployeeForm';
import EmployeeList from './EmployeeList';

const App = () => {
  const [employees, setEmployees] = useState([]);

  
  const fetchEmployees = async () => {
    try {
      const response = await axios.get('http://localhost:8002/api/emp/list/');
      setEmployees(response.data);
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    fetchEmployees();
  }, [employees]);

  const handleEmployeeAdded = async() => {
    fetchEmployees(); // Update the employee list
  };

  return (
    <div>
      <EmployeeForm onEmployeeAdded={handleEmployeeAdded} setEmployees={setEmployees}/>
      <EmployeeList employees={employees} />
    </div>
  );
};

export default App;
