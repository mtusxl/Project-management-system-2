from django.contrib import admin

from Project_Management_System.Dashbords.models import Column, Dashbord

from .models import Task


class ColumnInline(admin.TabularInline):
    model = Column
    fields = ["name"]


class DashboardInline(admin.TabularInline):
    model = Dashbord
    fields = ["name"]


@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "status",
        "priority",
        "deadline",
        "executor",
        "hours",
        "sprint",
    ]
    list_select_related = ["column"]
    search_fields = ["name", "project"]
    ordering = ["priority", "deadline"]
