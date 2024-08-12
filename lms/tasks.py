import smtplib

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, Subscription


@shared_task
def send_message(pk):
    instance = Course.objects.filter(pk=pk).first()

    subs = Subscription.objects.all().filter(course=instance)
    for u in subs:
        try:
            send_mail(
                subject="Обновление курса",
                message=f"Материалы курса {instance.title} обновлены.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[u.user],
                fail_silently=False,
            )
        except smtplib.SMTPException as error:
            raise error
