import random

from celery import shared_task


@shared_task
def send_code(number):
    verification_code = random.randint(1000, 9999)
    print(f"Код {verification_code} отправлен на номер {number}")
