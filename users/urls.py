from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListApiView, UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentsListApiView.as_view(), name="lesson_list"),
    path("register/", UserCreateAPIView.as_view(), name="register_user"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
