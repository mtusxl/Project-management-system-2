from django.db import models

from .base_model import BaseDashbord


class Dashbord(BaseDashbord):
    name = models.CharField(max_length=255, blank=True,  null=True)
    column = models.CharField(max_length=100, blank=True,  null=True, verbose_name="колонка")
    project = models.ManyToManyField(
        "Projects.Project", related_name="dashbords"
    )

    def __str__(self):
        return self.column
