from django.db import models


class BaseNotification(models.Model):
    update_date = models.DateField()
