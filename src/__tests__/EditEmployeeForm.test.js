// EditEmployeeForm.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EditEmployeeForm from '../EditEmployeeForm';


describe('EditEmployeeForm', () => {
  const mockEmployee = { id: 1, name: 'John Doe', birthdate: '1990-01-01', department: 'HR', salary: '50000' };
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  test('renders form fields with employee data', () => {
    render(<EditEmployeeForm employee={mockEmployee} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
    expect(screen.getByDisplayValue('1990-01-01')).toBeInTheDocument();
    expect(screen.getByDisplayValue('HR')).toBeInTheDocument();
    expect(screen.getByDisplayValue('50000')).toBeInTheDocument();
  });

  test('submits the form with updated data', () => {
    render(<EditEmployeeForm employee={mockEmployee} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    fireEvent.change(screen.getByLabelText('Name:'), { target: { value: 'John Updated' } });

    fireEvent.click(screen.getByText('Save'));

    expect(mockOnSubmit).toHaveBeenCalledWith({ ...mockEmployee, name: 'John Updated' });
  });

  test('calls onCancel when cancel button is clicked', () => {
    render(<EditEmployeeForm employee={mockEmployee} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    fireEvent.click(screen.getByText('Cancel'));

    expect(mockOnCancel).toHaveBeenCalled();
  });
});

