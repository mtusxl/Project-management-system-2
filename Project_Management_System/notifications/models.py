from datetime import date
from django.db import models

from .base_model import BaseNotification

# from Users.models import User


class Notification(BaseNotification):
    recipientv = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="notification",
        verbose_name="получатель",
    )
    reminder_date = models.DateField(verbose_name="дата напоминания", default=date.today)
    message = models.TextField(verbose_name="сообщение")

    def __str__(self):
        return f"{self.recipientv}: {self.message}"
