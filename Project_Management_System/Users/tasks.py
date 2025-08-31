import logging
import random

import sentry_sdk
from celery import shared_task

from Project_Management_System.config.settings.base import REDIS_CLIENT

r_client = REDIS_CLIENT
logger = logging.getLogger("celery")


@shared_task
def send_code(number):
    sentry_sdk.set_tag("component", "celery")
    sentry_sdk.set_tag("task_name", "send_code")
    try:
        logger.info("Задача send_code запущена")
        code = random.randint(1000, 9999)
        logger.debug(f"Генерация кода для номера {number}: {code}")
        r_client.set(f"verify_code:{number}", code, ex=300)
        logger.info("Custom Celery log")
        logger.info(
            f"Код {code} отправлен на номер {number} и сохранён в Redis (ключ: verify_code:{number})"  # noqa E501
        )
    except Exception as e:
        logger.error(f"Ошибка в задаче: {str(e)}")
        sentry_sdk.capture_exception(e)
        raise
