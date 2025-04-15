import pyotp
from apps.users.models import Profile
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import (
    LoginForm,
    RegistrationForm,
    Verify2FAForm,
)
from .utils import generate_qrcode, generate_totp_uri

User = get_user_model()


class LoginView(FormView):
    """Аутентификация User."""

    form_class = LoginForm
    template_name = "auth/login.html"
    extra_context = {"title": "Вход в аккаунт"}

    def form_valid(self, form):
        user = form.get_user()

        if user.is_mfa_enabled:
            self.request.session["mfa_user_pk"] = user.pk
        else:
            login(self.request, user=user)

        messages.success(self.request, "Вы успешно вошли в систему.")
        return super().form_valid(form)

    def form_invalid(self, form):
        result = super().form_invalid(form)
        for error in form.errors:
            messages.error(self.request, form.errors[error].as_text())
        return result

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})
        else:
            return reverse("auth:verify_2fa")


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

        if not user.mfa_hash:
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

        totp = pyotp.TOTP(user.mfa_hash or user.get_mfa_hash())

        if totp.verify(token, valid_window=1):
            if "mfa_user_pk" in self.request.session:
                del self.request.session["mfa_user_pk"]
                login(self.request, user)
                messages.success(self.request, "Вы успешно вошли в систему.")
        else:
            messages.error(self.request, "Неверный токен. Пожалуйста, попробуйте снова.")
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})


class RegistrationView(FormView):
    """Вьюха для регистрации User."""

    form_class = RegistrationForm
    template_name = "auth/register.html"
    extra_context = {"title": "Регистрация пользователя"}

    def form_valid(self, form):
        result = super().form_valid(form)

        user = form.save(commit=False)
        is_mfa_enabled = form.cleaned_data["is_mfa_enabled"]

        if is_mfa_enabled:
            user.is_mfa_enabled = True
            user.mfa_hash = pyotp.random_base32()

        user.save()
        Profile.objects.create(user=user)
        messages.success(self.request, "Аккаунт пользователя успешно создан.")

        if is_mfa_enabled:
            self.request.session["mfa_user_pk"] = user.pk
            messages.success(self.request, "Настройте 2FA с помощью Google Authenticator или аналогичного приложения.")
            return redirect("auth:qrcode")
        else:
            login(self.request, user)
            messages.success(self.request, "Вы успешно вошли в систему.")
            if "mfa_user_pk" in self.request.session:
                del self.request.session["mfa_user_pk"]
            return redirect("users:profile", pk=user.pk)

        return result

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return redirect("auth:register")

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})
        else:
            return reverse("auth:login")


class QrCodeView(FormView):
    """Генерация QR-кода для регистрации."""

    template_name = "auth/qrcode.html"
    form_class = Verify2FAForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.request.session.get("mfa_user_pk"))

        if not user.mfa_hash:
            user.mfa_hash = pyotp.random_base32()
            user.save()

        totp_uri = generate_totp_uri(user=user, secret_key=user.mfa_hash)

        img_str = generate_qrcode(totp_uri)

        context["qr_code_img"] = f"data:image/png;base64,{img_str}"
        context["hash"] = user.mfa_hash
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        user = get_user_model().objects.get(pk=self.request.session.get("mfa_user_pk"))
        token = form.cleaned_data["token"]

        # Проверка токена
        totp = pyotp.TOTP(user.mfa_hash)
        if totp.verify(token):
            if "mfa_user_pk" in self.request.session:
                del self.request.session["mfa_user_pk"]
            messages.success(self.request, "2FA успешно настроена!")
        else:
            messages.error(self.request, "Неверный токен. Пожалуйста, попробуйте снова.")
            return super().form_invalid(form)

        return result

    def form_invalid(self, form):
        result = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return result

    def get_success_url(self):
        return reverse("auth:login")


class LogoutUserView(View):
    """Вью для выхода User."""

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы вышли из системы.")
        return redirect("auth:login")
