from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    update_date = models.DateField()
