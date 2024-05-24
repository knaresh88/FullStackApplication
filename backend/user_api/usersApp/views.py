# views.py
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer

from rest_framework.views import APIView
from django.shortcuts import render
import os
import subprocess



api_key = "2718c06a-a451-4d73-ad10-cfcf168a8e94"
cf = CfClient(api_key)
cf.wait_for_initialization()


def is_feature_enabled(flag_key, target_identifier, target_name, default=False):
    target = Target(identifier=target_identifier, name=target_name)
    return cf.bool_variation(flag_key, target, default)



class CreateUser(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        feature_enabled = is_feature_enabled('GitHubActionsFlag','Naresh','Git-Actions', False)
        if not feature_enabled:
            return JsonResponse({'message': 'This feature flag is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return super().create(request, *args, **kwargs)


class EditUser(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def update(self, request, *args, **kwargs):
        feature_enabled = is_feature_enabled('GitHubActionsFlag','Naresh','Git-Actions', False)
        if not feature_enabled:
            return JsonResponse({'message': 'This feature flag is disabled'}, status=403)
        else:
            return super().update(request, *args, **kwargs)


class DeleteUser(APIView):
    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        
        feature_enabled = is_feature_enabled('GitHubActionsFlag', 'Naresh', 'Git-Actions', False)
        if not feature_enabled:
            return JsonResponse({'message': 'This feature flag is disabled'}, status=status.HTTP_403_FORBIDDEN)
        
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise JsonResponse({'message': 'Employee does not exist'}, status=status.HTTP_404_NOT_FOUND)




class ListUsers(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        feature_enabled = is_feature_enabled('Flag2', 'Naresh', 'Git-Actions', False)
        if not feature_enabled:
            return Response({'message': 'This feature flag is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Get the queryset
            queryset = self.get_queryset()
            # Serialize the queryset
            serializer = self.get_serializer(queryset, many=True)
            # Return the serialized data as JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
