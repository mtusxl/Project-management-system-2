from django.dispatch import Signal, receiver

from .tasks import send_code

verification_code_requested = Signal()


@receiver(verification_code_requested)
def verify_numver(sender, number, **kwargs):
    send_code.delay(number)
