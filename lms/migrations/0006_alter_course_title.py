# Generated by Django 5.0.7 on 2024-07-26 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0005_alter_lesson_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="title",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="название"
            ),
        ),
    ]
