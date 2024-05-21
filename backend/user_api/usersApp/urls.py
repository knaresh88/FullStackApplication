# usersApp/urls.py
from django.urls import path
from .views import CreateUser, EditUser, DeleteUser, ListUsers

urlpatterns = [
    path('emp/', CreateUser.as_view(),name= 'create-user'),  # Endpoint for creating a user
    path('emp/<int:pk>/', EditUser.as_view(), name='edit-user'),  # Endpoint for editing a user
    path('emp/<int:pk>/delete/', DeleteUser.as_view(), name='delete-user'),  # Endpoint for deleting a user
    path('emp/list/', ListUsers.as_view(), name='list-users'),  # Endpoint for retrieving all users
]

