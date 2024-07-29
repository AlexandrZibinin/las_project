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
    DestroyAPIView, get_object_or_404,
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
    pagination_class = CustomPagination



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


class SubscriptionAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        print(subscription)
        if not created:
            subscription.delete()
            message = 'Subscription removed'
        else:
            message = 'Subscription added'

        return Response({"message": message}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

