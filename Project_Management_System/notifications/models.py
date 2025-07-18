from django.db import models

# from Users.models import User


class Notification(models.Model):
    recipientv = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="notification",
        verbose_name="получатель",
    )
    reminder_date = models.DateField(verbose_name="дата напоминания")
    message = models.TextField(verbose_name="сообщение")

    def __str__(self):
        return f"{self.recipientv}: {self.message}"
