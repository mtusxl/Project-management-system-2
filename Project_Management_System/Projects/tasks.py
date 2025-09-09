import json
import logging

from celery import shared_task
from django.core.cache import cache
from django.db.models import Q

from Project_Management_System.Projects.models import Project
from Project_Management_System.Projects.serializers import ProjectSerializer
from utils.cache_utils import generate_cache_key

logger = logging.getLogger("celery")


@shared_task
def warm_project_cache(self):
    try:
        queryset = (
            Project.objects.filter(Q(author__is_active=True) | Q(members__is_active=True))
            .distinct()
            .select_related("author")
            .prefetch_related("members")[:50]
        )
        data = ProjectSerializer(queryset, many=True).data
        unique_authors = set(project["author"] for project in data if "author" in project)

        for author_id in unique_authors:
            author_data = [project for project in data if project["author"] == author_id]
            cache_key = generate_cache_key(
                prefix="projects", url="api/projects", user_id=str(author_id)
            )
            cache.set(cache_key, json.dumps(author_data), timeout=1800)
        print("Cache warm up completed")
        logger.info("Cache warm up completed!")
    except Exception as e:
        print("error cache warm up")
        logger.error("error cache warm up - ", str(e))
        raise self.retry(exc=e, countdown=30)
