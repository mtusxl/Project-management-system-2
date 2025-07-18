from django.contrib.auth.models import BaseUserManager
from django.db import models

from .base_model import BaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, number, password=None, **extra_fields):
        if not number:
            raise ValueError("The Number must be set")
        user = self.model(number=number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(number, password, **extra_fields)


class User(BaseUser):
    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        unique=False,
        default=None,
    )

    number = models.CharField(max_length=12, unique=True, verbose_name="номер телефона")
    USERNAME_FIELD = "number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.number
