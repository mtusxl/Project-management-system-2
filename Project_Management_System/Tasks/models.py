from django.db import models

# from Users.models import User


class Task(models.Model):
    PRIORITY_CHOICES = (
        (1, "Высокий"),
        (2, "Средний"),
        (3, "Низкий"),
    )
    name = models.CharField(verbose_name="название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, blank=True, null=True, verbose_name="приоритет"
    )
    deadline = models.DateField(null=True, blank=True, verbose_name="дедлайн")
    executor = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="task",
        verbose_name="оSтвественный",
    )
    hours = models.DurationField(verbose_name="время выполнения")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subtasks', on_delete=models.CASCADE)
    author = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name="task")

    def __str__(self):
        return self.name
