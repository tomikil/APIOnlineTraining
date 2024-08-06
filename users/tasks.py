from datetime import timezone, datetime, timedelta

import pytz
from celery import shared_task

from users.models import User


@shared_task
def check_user_activity():
    users = User.objects.filter(is_active=True)
    now = datetime.now(timezone.utc)
    deactivated_time = timedelta(days=30)
    for user in users:
        if user.last_login:
            if now - user.last_login > deactivated_time:
                user.is_active = False
                user.save()
                print(f"Пользователь {user} заблокирован")

