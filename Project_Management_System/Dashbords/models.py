from django.db import models


class Dashbord(models.Model):
    name = models.CharField(max_length=255)
    column = models.CharField(verbose_name="колонка")
    project = models.ManyToManyField('Projects.Project', on_delete=models.CASCADE, related_name='dashbords')


    def __str__(self):
        return self.column
