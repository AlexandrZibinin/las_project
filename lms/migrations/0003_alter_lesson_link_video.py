# Generated by Django 5.0.7 on 2024-07-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0002_alter_course_options_alter_lesson_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="link_video",
            field=models.URLField(
                blank=True, max_length=150, null=True, verbose_name="название"
            ),
        ),
    ]
