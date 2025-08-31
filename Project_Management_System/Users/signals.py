import logging

import sentry_sdk
from django.dispatch import Signal, receiver

from Project_Management_System.config.celery import app as celery_app
from Project_Management_System.Users.tasks import send_code

conn = celery_app.connection()
conn.ensure_connection()  # Force connect

verification_code_requested = Signal()
logger = logging.getLogger("celery")


@receiver(verification_code_requested)
def verify_numver(sender, number, **kwargs):
    logger.info("Сигнал сработал, пробуем отправить задачу Celery")
    sentry_sdk.set_tag("component", "celery")
    sentry_sdk.set_tag("error_type", "connection_refused")
    sentry_sdk.set_context("redis", {"host": "redis", "port": 6379, "db": 0})
    try:
        send_code.delay(number)  # Если здесь refused, лог выше всё равно уйдёт в Sentry
    except Exception as e:
        logger.error(f"Ошибка при .delay(): {str(e)}")  # Лог ошибки
        sentry_sdk.capture_exception(e)  # Захват исключения
