from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(AuthenticationForm):
    """Форма для входа пользователя."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", 'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", 'placeholder': 'Пароль'
    }))


class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя."""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", 'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", 'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш e-mail'}),
        }

