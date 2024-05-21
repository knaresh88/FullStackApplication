// App.test.js
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import App from '../App.js';

jest.mock('axios');

describe('App', () => {
  const mockEmployees = [
    { id: 1, name: 'John Doe', birthdate: '1990-01-01', department: 'HR', salary: '50000' },
    { id: 2, name: 'Jane Smith', birthdate: '1985-05-15', department: 'Finance', salary: '60000' },
  ];

  beforeEach(() => {
    axios.get.mockResolvedValue({ data: mockEmployees });
  });

  test('renders EmployeeForm and EmployeeList', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getAllByText('Add Employee')).toHaveLength(2); // Adjust the expected length based on your component structure
      expect(screen.getByText('Employee List')).toBeInTheDocument();
    });
  });
});