from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LessonValidator(field='url_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lesson_in_course = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)

    def get_count_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, course):
        user = self.context.get('request').user
        course = self.context.get('view').kwargs.get('pk')
        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription.exists():
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = ('title', 'description', 'preview', 'count_lesson_in_course', 'lesson', 'subscription')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
