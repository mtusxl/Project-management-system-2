from django.db import models
from Projects.models import Project

from .base_model import BaseAnalytics


# from Users.models import User
class ProjectMetrics(BaseAnalytics):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="проект")
    date = models.DateField(auto_now_add=True, verbose_name="Дата создания метрики")
    total_task = models.PositiveIntegerField(default=0, verbose_name="Всего задач")
    overdue_task = models.PositiveIntegerField(
        default=0, verbose_name="Просрочные задачи"
    )
    completed_task = models.PositiveIntegerField(
        default=0, verbose_name="Выполненные задачи"
    )


class UserPerformance(BaseAnalytics):
    user = models.ForeignKey(
        "Users.User", on_delete=models.CASCADE, verbose_name="Участник проекта"
    )
    total_projects = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во проектов"
    )
    total_task = models.PositiveIntegerField(default=0, verbose_name="Кол-во задач")
    completed_tasks = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во выполненных задач"
    )
    tasks_overdue = models.PositiveIntegerField(default=0)
    tasks_assigned = models.PositiveIntegerField(default=0)


class Report(BaseAnalytics):
    REPORT_FORMATS = (
        ("PDF", "PDF"),
        ("CSV", "CSV"),
        ("XLSX", "Excel"),
    )
    name = models.CharField(verbose_name="название отчета", blank=True)
    format = models.CharField(
        choices=REPORT_FORMATS, default="CSV", verbose_name="формат отчета"
    )
    file = models.FileField(upload_to="reports/")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("Users.User", on_delete=models.SET_NULL, null=True)


class ScheduledReport(BaseAnalytics):
    FREQUENCY_CHOICES = (
        ("daily", "Ежедневно"),
        ("weekly", "Еженедельно"),
        ("monthly", "Ежемесячно"),
    )

    report_id = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name="Отчет")

    recipients = models.ManyToManyField("Users.User", verbose_name="Получатели")

    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, verbose_name="Периодичность"
    )

    next_send = models.DateTimeField(verbose_name="Следующая отправка")

    is_active = models.BooleanField(default=True, verbose_name="Активно")
