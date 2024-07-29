from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from lms.models import Course, Lesson
from lms.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwnerOrReadOnly


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator, IsAuthenticated, )
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator | IsAuthenticated, IsOwnerOrReadOnly, )
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsAuthenticated, IsOwnerOrReadOnly, )

        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()



class LessonCreateApiView(CreateAPIView):
    permission_classes = [~IsModerator, IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsModerator]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer



class LessonRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsModerator]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer




class LessonUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer




class LessonDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, ~IsModerator]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
