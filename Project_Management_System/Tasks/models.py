from datetime import timedelta

from django.db import models

from .base_model import BaseTask

# from Users.models import User


class Task(BaseTask):
    PRIORITY_CHOICES = (
        (1, "Высокий"),
        (2, "Средний"),
        (3, "Низкий"),
    )
    STATUS_COICE = (("to_do", "To Do"), ("in_progress", "In progress"), ("done", "done"))
    name = models.CharField(verbose_name="название задачи", default="Без названия")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, blank=True, null=True, verbose_name="приоритет"
    )
    deadline = models.DateField(null=True, blank=True, verbose_name="дедлайн")
    executor = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="task_execor",
        verbose_name="отвественный",
    )
    hours = models.DurationField(verbose_name="время выполнения", default=timedelta(0))
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="subtasks", on_delete=models.CASCADE
    )
    column = models.ForeignKey(
        "Dashbords.Column",
        on_delete=models.CASCADE,
        related_name="tasks_column",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="task_author",
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "Projects.Project",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="tasks_project",
        verbose_name="id проекта",
    )
    status = models.CharField(
        choices=STATUS_COICE, verbose_name="Статус", default="to_do"
    )
    story_points = models.PositiveIntegerField(default=0, verbose_name="Очки")
    sprint = models.ForeignKey(
        "analytics.Sprint",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="tasks_sprint",
        verbose_name="спринт",
    )

    def __str__(self):
        return self.name
