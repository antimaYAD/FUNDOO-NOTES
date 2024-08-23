from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from time import sleep

@shared_task
def send_email_task(email_subject, email_body, recipient_email):
    send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    
    
