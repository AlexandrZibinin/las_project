from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE
from lms.models import Course, Lesson

METHOD_CHOICES = {
    "cash": "Наличные",
    "transfer": "Перевод на счет",
}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="телефон")
    city = models.CharField(max_length=35, **NULLABLE, verbose_name="город")
    avatar = models.ImageField(
        upload_to="users/avatars", **NULLABLE, verbose_name="аватар"
    )
    last_login = models.DateField(verbose_name="дата последнего входа", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Пользователь"
    )
    pay_day = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс"
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name="Оплаченный урок"
    )
    amount = models.IntegerField(verbose_name="Сумма к оплате")
    pay_method = models.CharField(choices=METHOD_CHOICES, verbose_name="Метод оплаты")
    session_id = models.CharField(max_length=255, **NULLABLE, verbose_name="Id сессии")
    pay_link = models.URLField(
        max_length=500, **NULLABLE, verbose_name="Ссылка на оплату"
    )

    def __str__(self):
        return f"{self.user} {self.pay_day}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
