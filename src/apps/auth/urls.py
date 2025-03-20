from django.urls import include, path, re_path

from .views import login_registration, login_user, logout_user, registration


app_name = "auth"

urlpatterns = [
    path('login_registration/', login_registration, name='login_registration'),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", registration, name="register"),
]
