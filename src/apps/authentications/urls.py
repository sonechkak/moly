from django.urls import path

from .views import (
    LoginView,
    LogoutUserView,
    QrCodeView,
    RegistrationView,
    Verify2FAView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("qrcode/", QrCodeView.as_view(), name="qrcode"),
    path("verify_2fa/", Verify2FAView.as_view(), name="verify_2fa"),
]
