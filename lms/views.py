from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer
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



