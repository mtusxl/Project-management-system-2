from django.db import models

from .base_model import BaseModel


class Dashbord(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    project = models.ManyToManyField("Projects.Project", related_name="dashbords")

    def __str__(self):
        return self.name


class Column(BaseModel):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    dashbord = models.ForeignKey(
        Dashbord, on_delete=models.CASCADE, related_name="columns"
    )

    def __str__(self):
        return self.name
