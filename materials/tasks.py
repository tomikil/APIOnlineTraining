from celery import shared_task
from django.core.mail import send_mail

from materials.models import Subscription
from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_update_course(course_id):
    """Отправка уведомления об обновлении курса"""
    subscription = Subscription.objects.filter(course=course_id)
    for sub in subscription:
        course = sub.course
        user = sub.user
        send_mail(
            subject=f'Обновление в курса: {course.title}',
            message=f'В курс "{course.title}" произведено обновление',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f'Отправлено уведомление пользователю {user.email} об обновлении курса {course.title}')