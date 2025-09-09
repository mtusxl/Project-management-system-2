import json
import logging

from celery import shared_task
from django.core.cache import cache
from django.db.models import Q

from Project_Management_System.Tasks.models import Task
from Project_Management_System.Tasks.serializers import TaskSerializer
from utils.cache_utils import generate_cache_key

logger = logging.getLogger("celery")


@shared_task
def warm_tasks_cache(self):
    try:
        queryset = (
            Task.objects.filter(Q(author__is_active=True) | Q(executor__is_active=True))
            .distinct()
            .select_related("author", "executor")[:50]
        )
        data = TaskSerializer(queryset, many=True).data
        unique_authors = set(task["author"] for task in data if "author" in task)

        for author_id in unique_authors:
            author_data = [task for task in data if task["author"] == author_id]
            cache_key = generate_cache_key(
                prefix="tasks", url="api/tasks", user_id=str(author_id)
            )
            cache.set(cache_key, json.dumps(author_data), timeout=1800)
        logger.info("Cahe Warm up for tasks completed!")
    except Exception as e:
        logger.error("error warm up for tasks")
        raise self.retry(exc=e, countdown=30)
