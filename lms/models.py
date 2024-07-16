from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=25, verbose_name='название')
    preview = models.ImageField(upload_to='lms/images', blank=True, null=True, verbose_name='превью')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    lesson = models.ForeignKey('Lesson', blank=True, null=True, on_delete=models.CASCADE, verbose_name='урок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=25, verbose_name='название')
    preview = models.ImageField(upload_to='lms/images', blank=True, null=True, verbose_name='превью')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    link_video = models.CharField(max_length=150, verbose_name='название')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

