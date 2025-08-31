from django.urls import path

from Project_Management_System.Users.api import RegistAPI, Test_API

urlpatterns = [
    path("api/register/", RegistAPI.as_view(), name="register"),
    path("api/test_api", Test_API.as_view(), name="Test API"),
]
