from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        payment = Payment.objects.create(
            user=User.objects.get(id=1),
            payment_lesson=Lesson.objects.get(id=2),
            sum_payment='600',
            payment_method='переводом'
        )
        payment.save()
