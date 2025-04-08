import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.users.models import Profile


@pytest.mark.django_db
def test_login_view(client, user):
    """Тест для LoginView."""

    url = reverse("auth:login")
    response = client.post(url, {
        "username": user.username,
        "password": "StrongPassword123!",
    })
    assert response.status_code == 302
    assert response.url == reverse("users:profile", kwargs={"pk": user.id})

@pytest.mark.django_db
def test_registration_view(client):
    """Тест для RegistrationView."""

    url = reverse("auth:register")
    response = client.post(url, {
        "username": "test_user",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
    })
    assert response.status_code == 302

    user_model = get_user_model()
    user = user_model.objects.get(username="test_user")

    assert response.url == reverse("users:profile", kwargs={"pk": user.id})
    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_logout_view(client, user):
    """Тест для LogoutView."""

    url = reverse("auth:logout")
    client.login(username=user.username, password="StrongPassword123!")
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("auth:login")

@pytest.mark.django_db
def test_login_view_invalid_credentials(client):
    """Тест для LoginView с неверными учетными данными."""

    url = reverse("auth:login")
    response = client.post(url, {
        "username": "invalid_user",
        "password": "invalid_password",
    })

    assert response.status_code == 302
    assert response.url == reverse("auth:login")

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
