from django.urls import include, path, re_path

from .views import (
    LoginView,
    LogoutUserView,
    QrCodeView,
    RegistrationView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("qrcode/", QrCodeView.as_view(), name="qrcode"),
]
