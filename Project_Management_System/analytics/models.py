from datetime import date

from django.db import models
from django.db.models import Q

from Project_Management_System.Projects.models import Project
from Project_Management_System.Tasks.models import Task

from .base_model import BaseAnalytics


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
    tasks_overdue = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во просроченных задач"
    )

    def calc_overdue_tasks(self):
        overdue = (
            Task.objects.filter(
                Q(executor=self.user) | Q(author=self.user), deadline__lt=date.today()
            )
            .exclude(status="done")
            .count()
        )
        self.tasks_overdue = overdue
        self.save()
        return overdue

    def __str__(self):
        return f"{self.user.username}"


class Sprint(BaseAnalytics):
    name = models.CharField(max_length=255, verbose_name="Название спринта")
    project = models.OneToOneField(
        "Projects.Project",
        on_delete=models.CASCADE,
        verbose_name="проект",
        related_name="sprint_project",
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True)
    planned_points = models.PositiveIntegerField(default=0, verbose_name="Очки на старте")
    completed_points = models.PositiveIntegerField(
        default=0, verbose_name="Завершенные очки"
    )

    def save(self, *args, **kwargs):
        self.calc_completed_points()
        self.calc_planned_points()
        super().save(*args, **kwargs)
        self.tasks_in_sprint()

    def calc_completed_points(self):
        tasks_in_sprint = Task.objects.filter(
            project=self.project,
            deadline__range=(self.start_date, self.end_date),
            status="done",
        )
        self.completed_points = sum(task.story_points for task in tasks_in_sprint)
        print(f"Завершенные очки - {self.completed_points}")
        return self.completed_points

    def calc_planned_points(self):
        tasks_in_sprint = Task.objects.filter(
            Q(status="to_do") | Q(status="in_progress"),
            project=self.project,
            deadline__range=(self.start_date, self.end_date),
        )
        self.planned_points = sum(task.story_points for task in tasks_in_sprint)
        print(f"Запланированные очки - {self.planned_points}")
        return self.planned_points

    def progress(self):
        if self.completed_points > 0:
            story_points = self.tasks_sprint.all()
            total_sp = sum(task.story_points for task in story_points)
            print(total_sp)
            progress = int((self.completed_points / total_sp) * 100)
            return f" {progress} %"
        else:
            return 0

    def tasks_in_sprint(self):
        tasks_in_sprint = Task.objects.filter(
            project=self.project, deadline__range=(self.start_date, self.end_date)
        )
        tasks_in_sprint.update(sprint=self)

        return tasks_in_sprint.count()

    def __str__(self):
        return f"{self.name}"


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
