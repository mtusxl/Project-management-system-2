from datetime import date

from django.contrib import admin
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from Tasks.models import Task

from .models import ProjectMetrics, Report, ScheduledReport, Sprint, UserPerformance

admin.site.register(ProjectMetrics)
admin.site.register(Report)
admin.site.register(ScheduledReport)


@receiver(post_save, sender=Task)
def update_user_perfomace(sender, instance, **kwargs):
    if instance.executor:
        perfomance, created = UserPerformance.objects.get_or_create(
            user=instance.executor
        )
        perfomance.total_task = instance.executor.task_execor.count()
        perfomance.completed_tasks = instance.executor.task_execor.filter(
            status="done"
        ).count()
        perfomance.tasks_overdue = (
            instance.executor.task_execor.filter(deadline__lt=date.today())
            .exclude(status="done")
            .count()
        )
        perfomance.save()


# @receiver(post_save, sender=Sprint)
# def update_sprint(sender, instance, **kwargs):
#     instance.completed_points = instance.calc_completed_points()
#     instance.planned_points = instance.calc_planned_points()


@admin.register(UserPerformance)
class Tasks_Metrics(admin.ModelAdmin):
    list_display = [
        "user",
        "to_do",
        "in_progress",
        "done",
        "total_points",
        "completed_tasks",
        "tasks_overdue",
    ]

    def to_do(self, obj):
        return (
            obj.user.task_execor.filter(status="to_do").aggregate(
                total=Sum("story_points")
            )["total"]
            or 0
        )

    def in_progress(self, obj):
        return int(
            obj.user.task_execor.filter(status="in_progress").aggregate(
                total=Sum("story_points")
            )["total"]
            or 0
        )

    def done(self, obj):
        return (
            obj.user.task_execor.filter(status="done").aggregate(
                total=Sum("story_points")
            )["total"]
            or 0
        )

    def total_points(self, obj):
        total_points = self.to_do(obj) + self.in_progress(obj) + self.done(obj)
        return total_points


class InlineTasks(admin.TabularInline):
    model = Task
    fields = ["name", "status", "executor", "deadline", "story_points"]
    extra = 0


@admin.register(Sprint)
class Sprint(admin.ModelAdmin):
    list_display = [
        "name",
        "project",
        "start_date",
        "end_date",
        "planned_points",
        "completed_points",
        "progress",
    ]
    inlines = [InlineTasks]
