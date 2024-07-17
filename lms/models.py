from django.db import models

from config.settings import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=25, verbose_name="название")
    preview = models.ImageField(
        upload_to="lms/images", **NULLABLE, verbose_name="превью"
    )
    description = models.TextField(**NULLABLE, verbose_name="описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=25, verbose_name="название")
    preview = models.ImageField(
        upload_to="lms/images", **NULLABLE, verbose_name="превью"
    )
    description = models.TextField(**NULLABLE, verbose_name="описание")
    link_video = models.URLField(max_length=150, **NULLABLE, verbose_name="название")
    course = models.ForeignKey(
        "Course",
        **NULLABLE,
        on_delete=models.CASCADE,
        verbose_name="курс",
        related_name="lessons",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
