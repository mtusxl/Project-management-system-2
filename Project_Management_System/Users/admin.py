from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "username",
        "first_name",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    readonly_fields = ["last_login", "is_active"]


admin.site.register(User, UserAdmin)
