from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.test")
        self.course = Course.objects.create(title="course1", owner=self.user)

        self.client.force_authenticate(user=self.user)


    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))

        data = {
            "title": "course1"
        }
        response = self.client.get(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {
            "title":"course2"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))

        data = {
            "title": "course2"
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), "course2"
        )

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )


    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


