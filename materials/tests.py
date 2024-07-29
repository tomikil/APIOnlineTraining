from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@admin.ru')
        self.course = Course.objects.create(title='Программирование web')
        self.lesson = Lesson.objects.create(title='PHP 5', course=self.course, owner=self.user,
                                            url_video='https://www.youtube.com/watch')
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создание уроков"""
        data = {
            'title': 'Test 1',
            'description': 'Test description',
            'course': self.lesson.course.id,
            'url_video': 'https://www.youtube.com/watch'
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data['title'],
            'Test 1'
        )
        self.assertEqual(
            response.data['description'],
            'Test description'
        )
        self.assertEqual(
            response.data['course'],
            self.lesson.course.id
        )
        self.assertEqual(
            response.data['owner'],
            self.user.id
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        self.url = reverse('materials:lesson_update', args=(self.lesson.pk,))
        self.data = {
            'title': 'Test 1 2024',
            'description': 'Test description 2024',
            'url_video': 'https://www.youtube.com/watch',
        }
        response = self.client.patch(self.url, self.data)
        self. data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            self.data['title'],
            'Test 1 2024'
        )
        self.assertEqual(
            self.data['description'],
            'Test description 2024'
        )
        self.assertEqual(
            self.data['course'],
            self.lesson.course.id
        )

    def test_retrieve_lesson(self):
        """Тестирование получения урока"""
        self.url = reverse('materials:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            self.lesson.title
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        self.url = reverse('materials:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """Тестирование получения списка уроков"""
        self.url = reverse('materials:lesson_list')
        response = self.client.get(self.url)
        self.data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data),
            4
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@user.ru')
        self.course = Course.objects.create(title='Программирование web')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('materials:subscription')

    def test_activate_subscription(self):
        """Тестирование активации подписки"""
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.all().count(), 1
        )
        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_deactivate_subscription(self):
        """Тестирование деактивации подписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(self.url, {'user': self.user.id, 'course': self.course.id})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.all().count(), 0
        )
