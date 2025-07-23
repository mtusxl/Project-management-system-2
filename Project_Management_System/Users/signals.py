from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User
from .tasks import send_code


@receiver(pre_save, sender=User)
def verify_numver(sender, instance, **kwargs):
    send_code.delay(instance.number)
