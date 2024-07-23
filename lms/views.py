from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
            self.permission_classes = (~IsModerator,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator | IsOwnerOrReadOnly,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsOwnerOrReadOnly,)

        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    permission_classes = [~IsModerator, IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer



class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer




class LessonUpdateAPIView(UpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer




class LessonDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, ~IsModerator]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
