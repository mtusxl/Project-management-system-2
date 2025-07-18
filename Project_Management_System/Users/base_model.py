from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    class Meta:
        abstract = True
    update_date = models.DateField(null=True)
    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        unique=False,
        default=None,
    )
