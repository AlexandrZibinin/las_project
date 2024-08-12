from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def last_login_check():
    today = timezone.now().today()
    last_enter = today - timedelta(days=30)
    print(last_enter)
    users = User.objects.filter(last_login__isnull=False, last_login=last_enter)
    for user in users:
        user.is_active = False
        user.save()
