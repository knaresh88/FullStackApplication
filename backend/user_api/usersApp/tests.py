# test.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee
from .serializers import EmployeeSerializer
from unittest.mock import patch


class EmployeeViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = {
            'name': 'John Doe',
            'birthdate': '1990-01-01',
            'department': 'IT',
            'salary': '50000.00'
        }
        self.employee = Employee.objects.create(**self.employee_data)
        self.url_create = reverse('create-user')
        self.url_edit = reverse('edit-user', kwargs={'pk': self.employee.pk})
        self.url_delete = reverse('delete-user', kwargs={'pk': self.employee.pk})
        self.url_list = reverse('list-users')

    @patch('usersApp.views.is_feature_enabled')
    def test_create_employee(self,mock_feature_enabled):
        mock_feature_enabled.return_value = True
        response = self.client.post(self.url_create, self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)  # Assuming one existing employee

    @patch('usersApp.views.is_feature_enabled')
    def test_edit_employee(self,mock_feature_enabled):
        mock_feature_enabled.return_value = True
        updated_data = {
            'name': 'Jane Doe',
            'birthdate': '1992-02-02',
            'department': 'HR',
            'salary': '60000.00'
        }
        response = self.client.put(self.url_edit, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'Jane Doe')

    @patch('usersApp.views.is_feature_enabled')
    def test_delete_employee(self, mock_feature_enabled):
        mock_feature_enabled.return_value = True
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    @patch('usersApp.views.is_feature_enabled')
    def test_list_employees(self,mock_feature_enabled):
        mock_feature_enabled.return_value = True
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = EmployeeSerializer(Employee.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    @patch('usersApp.views.is_feature_enabled')
    def test_disabled_feature_flag(self,mock_feature_enabled):
        mock_feature_enabled.return_value = False
        # Test when the feature flag is disabled
        response = self.client.post(self.url_create, self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(self.url_edit, self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
