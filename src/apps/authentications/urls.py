from django.urls import include, path, re_path

from .views import *

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("qrcode/", QrCodeView.as_view(), name="qrcode"),
    path("verify_2fa/", VerifyView.as_view(), name="verify_2fa"),
]
