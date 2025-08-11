from django.db import models

from .base_model import BaseProject


class Project(BaseProject):
    name = models.CharField(verbose_name="название проекта", blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="описание")
    author = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="project",
        verbose_name="автор проекта",
    )
    members = models.ManyToManyField(
        "Users.User",
        blank=True,
        related_name="projects_members",
        verbose_name="члены проекта",
    )

    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    def total_tasks(self):
        return self.tasks_project.count()

    def progress(self):
        tasks_done_count = self.tasks_project.filter(status="done").count()
        tasks_count = self.tasks_project.count()
        if tasks_count > 0:
            return f" {int((tasks_done_count / tasks_count) * 100)} %"
        return 0

    def __str__(self):
        return self.name
