// // EmployeeForm.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import EmployeeForm from '../EmployeeForm';

jest.mock('axios');

describe('EmployeeForm', () => {
  test('renders form fields correctly', () => {
    render(<EmployeeForm onEmployeeAdded={jest.fn()} setEmployees={jest.fn()} />);

    expect(screen.getByPlaceholderText('Name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Department')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Salary')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Name')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Add Employee/i })).toBeInTheDocument();
  });

  test('submits the form and handles success', async () => {
    const mockSetEmployees = jest.fn();
    const mockOnEmployeeAdded = jest.fn();
    axios.post.mockResolvedValue({ data: { id: 1, name: 'John Doe', birthdate: '1990-01-01', department: 'HR', salary: '50000' } });

    render(<EmployeeForm onEmployeeAdded={mockOnEmployeeAdded} setEmployees={mockSetEmployees} />);

    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByPlaceholderText('Department'), { target: { value: 'HR' } });
    fireEvent.change(screen.getByPlaceholderText('Salary'), { target: { value: '50000' } });
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'John Doe' } });

    fireEvent.click(screen.getByRole('button', { name: /Add Employee/i }));

    await waitFor(() => {
      expect(mockOnEmployeeAdded).toHaveBeenCalled();
      expect(mockSetEmployees).toHaveBeenCalledWith(expect.any(Function));
      expect(screen.getByText('Employee added successfully.')).toBeInTheDocument();
    });
  });

  test('handles error on form submission', async () => {
    axios.post.mockRejectedValue(new Error('Failed to add employee'));

    render(<EmployeeForm onEmployeeAdded={jest.fn()} setEmployees={jest.fn()} />);

    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByPlaceholderText('Department'), { target: { value: 'HR' } });
    fireEvent.change(screen.getByPlaceholderText('Salary'), { target: { value: '50000' } });
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'John Doe' } });

    fireEvent.click(screen.getByRole('button', { name: /Add Employee/i }));

    await waitFor(() => {
      expect(screen.getByText('Failed to add employee. Please try again.')).toBeInTheDocument();
    });
  });
});
