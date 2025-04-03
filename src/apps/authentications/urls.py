from django.urls import include, path, re_path

from .views import (
    LoginView,
    LogoutView,
    RegistrationView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
]
