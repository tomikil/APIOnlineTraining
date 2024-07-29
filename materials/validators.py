from rest_framework.serializers import ValidationError


class LessonValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tem_val = dict(value).get(self.field)
        if 'youtube.com' not in tem_val:
            raise ValidationError('Неверная ссылка, ссылка должна быть только на ресурс youtube.com')
