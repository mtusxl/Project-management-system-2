from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashbordAPI

router = DefaultRouter()

router.register(r"boards", DashbordAPI, basename="boards")


urlpatterns = [
    path("api/", include(router.urls)),
]
