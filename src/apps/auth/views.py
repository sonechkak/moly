from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import LoginForm, RegistrationForm


class LoginView(FormView):
    """Аутентификация User."""
    form_class = LoginForm
    template_name = "auth/login.html"
    extra_context = {"title": "Вход в аккаунт"}

    def form_valid(self, form):
        try:
            user = form.get_user()
            login(self.request, user)
            return redirect("users:profile", pk=user.pk)
        except Exception:
            messages.error(self.request, "Логин и пароль не совпадают")
            return redirect('auth:login')


class RegistrationView(FormView):
    """Вьюха для регистрации User."""
    form_class = RegistrationForm
    template_name = "auth/register.html"
    extra_context = {"title": "Регистрация пользователя"}

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            messages.success(self.request, "Аккаунт пользователя успешно создан")
            login(self.request, user=user)
            return redirect("users:profile", pk=user.pk)
        else:
            for error in form.errors:
                messages.error(self.request, form.errors[error].as_text())

        return redirect("auth:registration")


class LogoutView(LogoutView):
    """Вьюха для выхода User."""
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("auth:login")