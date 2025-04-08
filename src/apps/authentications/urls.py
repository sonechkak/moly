from django.urls import include, path, re_path

from .views import (
    LoginView,
    LogoutUserView,
    RegistrationView,
)

app_name = "auth"

urlpatterns = [
    path(r"^login/", LoginView.as_view(), name="login"),
    path(r"^logout/", LogoutUserView.as_view(), name="logout"),
    path(r"^register/", RegistrationView.as_view(), name="register"),
]
