// EditEmployeeForm.js
import React, { useState, useEffect } from 'react';

const EditEmployeeForm = ({ employee, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState(employee);

  useEffect(() => {
    setFormData(employee);
  }, [employee]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Edit Employee</h3>
      <label>
        Name:
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
        />
      </label>
      <label>
        Birthdate:
        <input
          type="date"
          name="birthdate"
          value={formData.birthdate}
          onChange={handleChange}
        />
      </label>
      <label>
        Department:
        <input
          type="text"
          name="department"
          value={formData.department}
          onChange={handleChange}
        />
      </label>
      <label>
        Salary:
        <input
          type="number"
          name="salary"
          value={formData.salary}
          onChange={handleChange}
        />
      </label>
      <button type="submit">Save</button>
      <button type="button" onClick={onCancel}>Cancel</button>
    </form>
  );
};

export default EditEmployeeForm;
