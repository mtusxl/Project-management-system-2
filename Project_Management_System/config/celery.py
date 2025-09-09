import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "Project_Management_System.config.settings.staging"
)

app = Celery(
    "project_management_system",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)
app.conf.beat_schedule = {
    "warm-project-cache": {
        "task": "Project_Management_System.Projects.tasks.warm_project_cache",
        "schedule": crontab(minute="0", hour="*/1"),
    },
    "warm-tasks-cache": {
        "task": "Project_Management_System.Tasks.tasks.warm_tasks_cache",
        "schedule": crontab(minute="0", hour="*/1"),
    },
}
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
