from .base import *  # noqa: F403,F401

DEBUG = True

ALLOWED_HOSTS = ["web", "localhost", "127.0.0.1", "0.0.0.0"]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")  # noqa: F405
    INSTALLED_APPS.append("debug_toolbar")  # noqa: F405
    INSTALLED_APPS.append("extra_settings")  # noqa: F405

    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

    EXTRA_SETTINGS_CACHE_NAME = "extra_settings"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/3",
        },
        "extra_settings": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "TIMEOUT": 300,
        },
    }


INTERNAL_IPS = ["127.0.0.1"]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


DEBUG_TOOLBAR_CONFIG = {
    "IS_RUNNING_TESTS": True,
    "SHOW_TEMPLATE_CONTEXT": True,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    "RESULTS_CACHE_SIZE": 100,
    "ENABLE_STACKTRACES": False,
    "UPDATE_ON_FETCH": True,
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
