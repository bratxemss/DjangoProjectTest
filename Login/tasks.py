from celery import shared_task
from django.core.mail import send_mail
from .models import ConfirmationCode
from random import randint
import logging

logging = logging.getLogger(__name__)

@shared_task
def send_welcome_email(email):
    send_mail(
        'Welcome!',
        'Thank you for registering on our website!',
        'example@gmail.com',
        [email],
        fail_silently=False,
    )
    logging.info("Sending welcome email")


@shared_task
def send_code_to_email(email):
    code = str(randint(100000, 999999))

    ConfirmationCode.objects.create(
        email=email,
        code=code
    )

    send_mail(
        'Welcome!',
        f'Thank you for registering on our website!. That is your code {code}',
        'example@gmail.com',
        [email],
        fail_silently=False,
    )

    logging.info(f"Sending code {code} to email {email}")
