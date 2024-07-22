# Generated by Django 5.0.7 on 2024-07-21 23:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0003_alter_lesson_link_video"),
        ("users", "0004_payments"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payments",
            options={"verbose_name": "Платеж", "verbose_name_plural": "Платежи"},
        ),
        migrations.AddField(
            model_name="payments",
            name="paid_lesson",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="lms.lesson",
                verbose_name="Оплаченный урок",
            ),
            preserve_default=False,
        ),
    ]
