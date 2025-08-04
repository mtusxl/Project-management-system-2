import random

from celery import shared_task

from Project_Management_System.settings.base import REDIS_CLIENT

r_client = REDIS_CLIENT


@shared_task
def send_code(number):
    code = random.randint(1000, 9999)
    r_client.set(f"verify_code:{number}", code, ex=300)
    print(f"Код {code} отправлен на номер {number}")
