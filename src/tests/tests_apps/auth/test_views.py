from django.urls import reverse


def test_login_view(client, user):
    """Тестируем вьюху для входа."""

    url = reverse("auth:login")
    response = client.post(url, {"username": user.username, "password": user.username})
    assert response.status_code == 302
    assert response.url == reverse("users:profile", kwargs={"pk": user.pk})
