from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Project_Management_System.Users"

    def ready(self):
        import Project_Management_System.Users.signals  # noqa: F401
