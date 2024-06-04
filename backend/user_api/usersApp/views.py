# views.py
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
import logging
from rest_framework.views import APIView
from django.shortcuts import render

api_key = 'fdbe6a44-f878-492c-a18c-f52f64687aba'

cf = CfClient(api_key)
cf.wait_for_initialization()

logger = logging.getLogger(__name__)


def is_feature_enabled(flag_key, target_identifier, target_name, default=False):
    target = Target(identifier=target_identifier, name=target_name)
    return cf.bool_variation(flag_key, target, default)
    
feature_enabled = is_feature_enabled('list_view', 'Naresh', 'Git-Actions', False)
logger.info(f"Feature flag 'crud' is set to: {feature_enabled}")

    # feature_enabled = cf.bool_variation(flag_key, target, default)
    # logger.debug(f'Feature flag "{flag_key}" for target "{target_identifier}-{target_name}": {feature_enabled}')
    # return feature_enabled

class FeatureFlagStatusView(APIView):
    def get(self, request, flag_key):
        target_identifier = 'Naresh'
        target_name = 'Git-Actions'
        feature_enabled = is_feature_enabled(flag_key, target_identifier, target_name, False)
        return JsonResponse({'feature_enabled': feature_enabled})
    
class CreateUser(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        feature_enabled = is_feature_enabled('My_Test_Flag','Naresh','Git-Actions', False)

        if not feature_enabled:
            return JsonResponse({'message': 'This feature flag is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return super().create(request, *args, **kwargs)


class EditUser(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def update(self, request, *args, **kwargs):
        feature_enabled = is_feature_enabled('My_Test_Flag','Naresh','Git-Actions', False)
        if not feature_enabled:
            return JsonResponse({'message': 'This feature flag is disabled'}, status=403)
        else:
            return super().update(request, *args, **kwargs)


class DeleteUser(APIView):
    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        
        feature_enabled = is_feature_enabled('My_Test_Flag', 'Naresh', 'Git-Actions', False)
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
        # feature_enabled = is_feature_enabled('list_view', 'Naresh', 'Git-Actions', False)
        feature_enabled = is_feature_enabled('list_view', 'Naresh', 'Git-Actions', False)

        if not feature_enabled:
            return Response({'message': 'This feature flag is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Get the queryset
            queryset = self.get_queryset()
            # Serialize the queryset
            serializer = self.get_serializer(queryset, many=True)
            # Return the serialized data as JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
