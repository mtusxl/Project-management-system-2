from django.db import models


class BaseTask(models.Model):
    update_date = models.DateField()
