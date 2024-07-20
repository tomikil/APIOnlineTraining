from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='наименование')
    preview = models.ImageField(upload_to='courses/course/image', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='наименование')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE, related_name='lesson')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='courses/lesson/image', verbose_name='картинка', **NULLABLE)
    url_video = models.CharField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f"{self.title}"
