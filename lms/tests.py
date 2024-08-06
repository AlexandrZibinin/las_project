from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.ru")
        self.course = Course.objects.create(title="course1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тест просмотр курса"""
        url = reverse("lms:course-detail", args=(self.course.pk,))

        data = {"title": "course1"}
        response = self.client.get(url, data)
        data = response.json()
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        """Тест создание курса"""
        url = reverse("lms:course-list")
        data = {"title": "course2"}
        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_update(self):
        """Тест изменение курса"""
        url = reverse("lms:course-detail", args=(self.course.pk,))

        data = {"title": "course2"}
        response = self.client.patch(url, data)
        data = response.json()
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "course2")

    def test_course_list(self):
        """Тест просмотр списка курса"""
        url = reverse("lms:course-list")
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subs_create(self):
        """Тест создание подписки"""
        url = reverse("lms:subs")
        response = self.client.post(url, args=(self.course.pk,))
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("message"), "Подписка добавлена")

    def test_subscriptions_delete(self):
        """Тест удаление подписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("lms:subs", args=(self.course.pk,))
        response = self.client.post(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("message"), "Подписка удалена")

    def test_course_delete(self):
        """Тест удаление курса"""
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)
