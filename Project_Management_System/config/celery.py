import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "Project_Management_System.config.settings.staging"
)

app = Celery(
    "project_management_system",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
