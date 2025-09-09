import logging

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from Project_Management_System.Projects.models import Project

logger = logging.getLogger("signals")


@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
def invalidation_projects_cache(sender, instance, **kwargs):
    try:
        user_id = instance.author.id if instance.author else None
        cache_key = f"projects:/api/projects/*:{user_id}"
        cache.delete(cache_key)
        logger.info(f"cache deleted for user with id: {user_id}")
    except Exception as e:
        logger.error(f"error in signals projects - {e}")
