from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectAPI

router = DefaultRouter()

router.register(r"projects", ProjectAPI, basename="projects")

urlpatterns = [
    path("api/", include(router.urls)),
]
