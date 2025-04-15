import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from apps.authentications.forms import RegistrationForm
from apps.users.models import Profile


User = get_user_model()


# @pytest.mark.django_db
# def test_login_view(client, user):
#     """Тест для LoginView."""
#     # Убедитесь, что пароль установлен корректно
#
#     user.set_password("StrongPassword123!")
#     user.is_active = True
#     user.save()
#
#     url = reverse("auth:login")
#     response = client.post(url, {
#         "username": user.username,
#         "password": "StrongPassword123!",
#     })
#
#     assert response.status_code == 302
#     assert response.url == reverse("users:profile", kwargs={"pk": user.pk})


@pytest.mark.django_db
def test_get_request_returns_form(client):
    """Проверяет, что GET-запрос возвращает форму."""
    url = reverse('auth:register')
    response = client.get(url)

    assert response.status_code == 200
    assert 'auth/register.html' in [t.name for t in response.templates]
    assert isinstance(response.context['form'], RegistrationForm)
    assert response.context['title'] == 'Регистрация пользователя'


# @pytest.mark.django_db
# def test_valid_registration_without_mfa(client, valid_registration_data):
#     """Тестирует успешную регистрацию без 2FA."""
#     url = reverse('auth:register')
#     response = client.post(url, valid_registration_data)
#
#     user = User.objects.get(username='test_user1')
#     profile = Profile.objects.get(user=user)
#
#     # Проверяем email в модели User, а не Profile
#     assert user.email == 'test@example.com'
#     assert not profile.is_mfa_enabled
#     assert profile.mfa_hash is None
#
#     messages = list(get_messages(response.wsgi_request))
#     assert str(messages[0]) == "Аккаунт пользователя успешно создан"
#     assert response.url == reverse('users:profile', kwargs={'pk': user.pk})


@pytest.mark.django_db
def test_valid_registration_with_mfa(client, valid_registration_data):
    """Тестирует успешную регистрацию с включенным 2FA."""
    data = valid_registration_data.copy()
    data['is_mfa_enabled'] = True

    url = reverse('auth:register')
    response = client.post(url, data, follow=True)

    user = User.objects.get(username='test_user1')
    profile = Profile.objects.get(user=user)

    assert profile.is_mfa_enabled
    assert profile.mfa_hash is not None
    assert client.session['mfa_user_pk'] == user.pk

    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Аккаунт пользователя успешно создан"
    assert str(messages[1]) == "Настройте 2FA с помощью Google Authenticator или аналогичного приложения."
    assert response.redirect_chain[-1][0] == reverse('auth:qrcode')


@pytest.mark.django_db
def test_invalid_registration(client, valid_registration_data):
    """Тестирует обработку невалидных данных."""
    invalid_data = valid_registration_data.copy()
    invalid_data.update({
        'email': 'invalid-email',
        'password1': 'short',
        'password2': 'mismatch'
    })

    url = reverse('auth:register')
    response = client.post(url, invalid_data)

    assert response.status_code == 302
    assert response.url == reverse('auth:register')
    messages = list(get_messages(response.wsgi_request))
    assert any("email" in str(msg) for msg in messages)


@pytest.mark.django_db
def test_profile_auto_creation(client, valid_registration_data):
    """Проверяет автоматическое создание профиля."""
    url = reverse('auth:register')
    client.post(url, valid_registration_data)

    user = User.objects.get(username='test_user1')
    assert hasattr(user, 'profile')
    assert user.profile is not None


@pytest.mark.django_db
def test_mfa_hash_generation(client, valid_registration_data):
    """Проверяет генерацию mfa_hash при включенном 2FA."""
    data = valid_registration_data.copy()
    data['is_mfa_enabled'] = True
    url = reverse('auth:register')
    client.post(url, data)

    profile = Profile.objects.get(user__username='test_user1')
    assert profile.mfa_hash is not None
    assert len(profile.mfa_hash) == 32


@pytest.mark.django_db
def test_logout_view(client, user):
    """Тест для LogoutView."""

    url = reverse("auth:logout")
    client.login(username=user.username, password="StrongPassword123!")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("auth:login")


# @pytest.mark.django_db
# def test_login_view_invalid_credentials(client):
#     """Тест для LoginView с неверными учетными данными."""
#
#     url = reverse("auth:login")
#     response = client.post(url, {
#         "username": "invalid_user",
#         "password": "invalid_password",
#     })
#
#     assert response.status_code == 302
#     assert response.url == reverse("auth:login")


@pytest.mark.django_db
def test_registration_view_invalid_data(client):
    """Тест для RegistrationView с неверными данными."""

    url = reverse("auth:register")
    response = client.post(url, {
        "username": "test_user",
        "password1": "StrongPassword123!",
        "password2": "DifferentPassword123!",
    })

    assert response.status_code == 302
    assert response.url == reverse("auth:register")
