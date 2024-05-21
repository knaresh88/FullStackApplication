import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import EmployeeList from '../EmployeeList';
import { act } from '@testing-library/react';

jest.mock('axios');

describe('EmployeeList', () => {
  const mockEmployees = [
    { id: 1, name: 'John Doe', birthdate: '1990-01-01', department: 'HR', salary: '50000' },
    { id: 2, name: 'Jane Smith', birthdate: '1985-05-15', department: 'Finance', salary: '60000' },
  ];

  beforeEach(() => {
    axios.get.mockResolvedValue({ data: mockEmployees });
  });

  test('renders employee list', async () => {
    render(<EmployeeList />);
    await axios.get.mock.results[0].value;

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    });
  });

  test('handles employee deletion', async () => {
    axios.delete.mockResolvedValue({});
    render(<EmployeeList />);

    await waitFor(() => {
      fireEvent.click(screen.getAllByText('Delete')[0]);
    });

    await waitFor(() => {
      expect(screen.queryByText('John Doe')).not.toBeInTheDocument();
    });
  });

  test('handles employee editing', async () => {
    render(<EmployeeList />);

    await waitFor(() => {
      fireEvent.click(screen.getAllByText('Edit')[0]);
    });

    await waitFor(() => {
      expect(screen.getByText('Edit Employee')).toBeInTheDocument();
    });

    // Wrap state updates in act()
    await act(async () => {
      fireEvent.change(screen.getByLabelText('Name:'), { target: { value: 'John Updated' } });
      fireEvent.click(screen.getByText('Save'));
    });

    await waitFor(() => {
      expect(screen.getByDisplayValue('John Updated')).toBeInTheDocument();
    });
  });
});
