from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.cache import cache

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Форма для входа пользователя."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя пользователя"})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}))


class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя."""

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваш никнейм"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваш e-mail"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтвердите пароль"})
    )
    is_mfa_enabled = forms.BooleanField(
        required=False, initial=False, label="Включить 2FA", widget=forms.CheckboxInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_mfa_enabled")


class Verify2FAForm(forms.Form):
    """Форма для верификации 2FA."""

    token = forms.CharField(
        label="Токен",
        max_length=6,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите токен"}),
    )
