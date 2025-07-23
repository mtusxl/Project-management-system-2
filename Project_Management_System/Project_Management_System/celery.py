import os

from celery import Celery
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project_Management_System.settings")

app = Celery(
    "project_management_system",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["Users"])


load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
