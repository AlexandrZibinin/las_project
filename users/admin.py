from django.contrib import admin

from users.models import User, Payments


@admin.register(User)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("email",)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pay_day",
    )
