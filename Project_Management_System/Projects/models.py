from Dashbords.models import Dashbord
from django.db import models

from .base_model import BaseProject


class Project(BaseProject):
    name = models.CharField(verbose_name="название проекта")
    description = models.TextField(blank=True, verbose_name="описание")
    author = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="project",
        verbose_name="автор проекта",
    )
    members = models.ManyToManyField(
        "Users.User", blank=True, related_name="projects", verbose_name="члены проекта"
    )
    dashbord = models.ForeignKey(
        Dashbord, on_delete=models.CASCADE, verbose_name="Канбан доска"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name
