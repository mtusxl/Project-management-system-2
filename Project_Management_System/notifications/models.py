from datetime import date

from django.db import models

from .base_model import BaseNotification

# from Users.models import User


class Notification(BaseNotification):
    recipient = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="notification",
        verbose_name="получатель",
    )
    reminder_date = models.DateField(verbose_name="дата напоминания", default=date.today)
    message = models.TextField(verbose_name="сообщение")
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipientv}: {self.message}"


class NotificationSettings(models.Model):
    user = models.OneToOneField("Users.User", on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
