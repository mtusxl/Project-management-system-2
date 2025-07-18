from django.db import models


class BaseProject(models.Model):
    update_date = models.DateField()
