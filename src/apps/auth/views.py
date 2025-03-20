from django.contrib import messages
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm


def login_registration(request):
    context = {
        "title": "Войти или зарегистрироваться",
        "login_form": LoginForm,
        "registration_form": RegistrationForm,
    }
    return render(request, "auth/login_registration.html", context)


def login_user(request):
    """Аутентификация пользователя."""
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:index')
        else:
            messages.error(request, "Логин и пароль не совпадают")
            return redirect('auth:login_registration')
    else:
        return redirect('auth:login')


def logout_user(request):
    """Выход пользователя."""
    if request.user.is_authenticated:
        logout(request)
    return redirect("shop:index")


def registration(request):
    """Регистрация пользователя."""
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Аккаунт пользователя успешно создан")
            login(request, user)
            return redirect("shop:index")
        else:
            for error in form.errors:
                messages.error(request, form.errors[error].as_text())

        return redirect("auth:login_registration")