from django.db import models


class BaseAnalytics(models.Model):
    class Meta:
        abstract = True
    update_date = models.DateField(null=True)
