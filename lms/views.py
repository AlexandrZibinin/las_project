from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwnerOrReadOnly


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsModerator)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, ~IsModerator)

        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


class LessonCreateApiView(CreateAPIView):
    permission_classes = (IsAuthenticated, ~IsModerator)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsModerator)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsModerator)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly | IsModerator)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, ~IsModerator)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class SubscriptionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        subs = Subscription.objects.filter(user=user, course=course)

        if subs.exists():
            subs.delete()
            result = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            result = "Подписка добавлена"

        return JsonResponse({"response": result})
