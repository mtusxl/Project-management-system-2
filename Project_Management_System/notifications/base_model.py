from django.db import models


class BaseNotification(models.Model):
    class Meta:
        abstract = True

    update_date = models.DateField(null=True)
