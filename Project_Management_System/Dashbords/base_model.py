from django.db import models


class BaseDashbord(models.Model):
    update_date = models.DateField()
