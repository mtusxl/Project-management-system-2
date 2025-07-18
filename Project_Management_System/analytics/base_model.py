from django.db import models


class BaseAnalytics(models.Model):
    update_date = models.DateField()
