from django.urls import path

from .api import RegistAPI

urlpatterns = [
    path("api/register/", RegistAPI.as_view(), name="register"),
]
