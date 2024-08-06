from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_resurce


class LessonSerializer(ModelSerializer):
    link_video = serializers.URLField(validators=[validate_resurce])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_course_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_count_course_lessons(self, instance):
        return Lesson.objects.filter(course=instance.id).count()

    def get_is_subscribed(self, instance):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = "__all__"
