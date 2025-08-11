from django.contrib import admin
from Tasks.models import Task

from .models import Project


class TaskInlines(admin.TabularInline):
    model = Task
    fields = [
        "name",
        "status",
        "priority",
        "deadline",
        "executor",
        "story_points",
        "sprint",
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "author",
        "update_date",
        "created_at",
        "display_dashboards",
        "total_tasks",
        "progress",
    ]
    readonly_fields = ["update_date"]
    inlines = [TaskInlines]
    filter_horizontal = ["members"]
    search_fields = ["number", "username", "email"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(f"query_set {qs}")
        return qs.prefetch_related("dashbords")

    def display_dashboards(self, obj):
        dashbords = obj.dashbords.all()  # Все дашборды проекта через related_name
        count = dashbords.count()
        if count == 0:
            return "Нет дашбордов"
        names = ", ".join([str(d) for d in dashbords])
        return f"Дашборды: {names}"
