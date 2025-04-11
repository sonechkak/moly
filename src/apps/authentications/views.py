from typing import get_origin

import pyotp
import qrcode
from apps.users.models import Profile
from apps.users.utils import generate_totp_uri
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView

from .forms import *
from .utils import generate_qrcode


class LoginView(FormView):
    """Аутентификация User."""

    form_class = LoginForm
    template_name = "auth/login.html"
    extra_context = {"title": "Вход в аккаунт"}

    def form_valid(self, form):
        user = form.get_user()
        profile = Profile.objects.get(user=user)

        if profile.is_mfa_enabled:
            self.request.session["mfa_user_pk"] = user.pk
            return redirect("auth:verify_2fa")

        login(self.request, user)
        return redirect("users:profile", pk=user.pk)

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error].as_text())
        return redirect("auth:login")


class Verify2FAView(FormView):
    """Подтверждение 2FA при входе."""

    template_name = "auth/verify_2fa.html"
    form_class = Verify2FAForm

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("mfa_user_pk"):
            messages.error(request, "Сессия истекла. Пожалуйста, войдите снова.")
            return redirect("auth:login")

        try:
            User.objects.get(pk=request.session.get("mfa_user_pk"))
        except User.DoesNotExist:
            messages.error(request, "Пользователь не найден.")
            return redirect("auth:login")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.request.session.get("mfa_user_pk"))

        if not user.profile.mfa_hash:
            messages.error(self.request, "2FA не настроена для этого пользователя.")
            return redirect("auth:login")

        context.update(
            {
                "title": "Подтверждение 2FA",
                "user": user,
            }
        )
        return context

    def form_valid(self, form):
        user = get_object_or_404(User, id=self.request.session.get("mfa_user_pk"))
        token = form.cleaned_data["token"].strip()

        totp = pyotp.TOTP(user.profile.mfa_hash or user.profile.get_mfa_hash())

        if totp.verify(token, valid_window=1):
            if "mfa_user_pk" in self.request.session:
                del self.request.session["mfa_user_pk"]
                login(self.request, user)
                messages.success(self.request, "Вы успешно вошли в систему.")
                return redirect("users:profile", pk=user.pk)
        messages.error(self.request, "Неверный токен. Пожалуйста, попробуйте снова.")
        return redirect("auth:verify_2fa")


class RegistrationView(FormView):
    """Вьюха для регистрации User."""

    form_class = RegistrationForm
    template_name = "auth/register.html"
    extra_context = {"title": "Регистрация пользователя"}

    def form_valid(self, form):
        user = form.save(commit=False)
        is_mfa_enabled = form.cleaned_data["is_mfa_enabled"]
        user.save()

        Profile.objects.create(
            user=user,
            is_mfa_enabled=is_mfa_enabled,
            mfa_hash=pyotp.random_base32() if is_mfa_enabled else None,
        )
        messages.success(self.request, "Аккаунт пользователя успешно создан")

        if is_mfa_enabled:
            self.request.session["mfa_user_pk"] = user.pk
            messages.success(self.request, "Настройте 2FA с помощью Google Authenticator или аналогичного приложения.")
            return redirect("auth:qrcode")

        login(self.request, user)
        return redirect("users:profile", pk=user.pk)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return redirect("auth:register")


class QrCodeView(FormView):
    """Генерация QR-кода для регистрации."""

    template_name = "auth/qrcode.html"
    form_class = Verify2FAForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get("mfa_user_pk")
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user_id)

        totp_uri = generate_totp_uri(user=user, secret_key=profile.get_mfa_hash())

        img_str = generate_qrcode(totp_uri)

        context["qr_code_img"] = f"data:image/png;base64,{img_str}"
        context["hash"] = profile.mfa_hash
        return context

    def form_valid(self, form):
        user = get_user_model().objects.get(pk=self.request.session.get("mfa_user_pk"))
        profile = Profile.objects.get(user=user)
        token = form.cleaned_data["token"]

        # Проверка токена
        totp = pyotp.TOTP(profile.mfa_hash)
        if totp.verify(token):
            if "mfa_user_pk" in self.request.session:
                del self.request.session["mfa_user_pk"]
            profile.save()
            messages.success(self.request, "2FA успешно настроена!")

        return redirect("auth:login")

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return redirect("auth:qrcode")


class LogoutUserView(LogoutView):
    """Вьюха для выхода User."""

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("auth:login")
