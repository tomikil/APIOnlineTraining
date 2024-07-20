from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f"{self.email}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='user')
    date_of_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс',
                                       related_name='Course', **NULLABLE)
    payment_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок',
                                       related_name='lesson', **NULLABLE)
    sum_payment = models.PositiveIntegerField(verbose_name='Сумма платежа')
    method_choices = {"наличными": "наличными", "переводом": "переводом"}
    payment_method = models.CharField(max_length=50, choices=method_choices, verbose_name='Способ оплаты')

    def __str__(self):
        return (f'{self.user}: {self.date_of_payment}, {self.sum_payment}, {self.payment_method}, '
                f'за {self.payment_course if self.payment_course else self.payment_lesson}')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'