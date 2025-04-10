import base64
from io import BytesIO

import pyotp
import qrcode
from apps.users.models import Profile
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import *


class LoginView(FormView):
    """Аутентификация User."""

    form_class = LoginForm
    template_name = "auth/login.html"
    extra_context = {"title": "Вход в аккаунт"}

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("users:profile", pk=user.pk)

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error].as_text())
        return redirect("auth:login")


class RegistrationView(FormView):
    """Вьюха для регистрации User."""

    form_class = RegistrationForm
    template_name = "auth/register.html"
    extra_context = {"title": "Регистрация пользователя"}

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Аккаунт пользователя успешно создан")
        return redirect("auth:qrcode")

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return redirect("auth:register")


class QrCodeView(FormView):
    """Генерация QR-кода."""

    template_name = "auth/qrcode.html"
    form_class = Verify2FAForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        mfa_hash = profile.get_mfa_hash()

        img = qrcode.make(mfa_hash)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        context.update(
            {
                "title": "Настройка 2FA",
                "qr_code_img": f"data:image/png;base64,{img_str}",
                "hash": profile.mfa_hash,
            }
        )
        return context

    def form_valid(self, form):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        token = form.cleaned_data["token"]

        totp = pyotp.TOTP(profile.mfa_hash)
        if totp.verify(token):
            profile.is_mfa_enabled = True
            profile.save()
            messages.success(self.request, "2FA успешно настроена!")
            return redirect("users:profile", pk=user.pk)
        else:
            messages.error(self.request, "Неверный код. Попробуйте ещё раз.")
            return self.form_invalid(form)


class LogoutUserView(LogoutView):
    """Вьюха для выхода User."""

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("auth:login")
