import pytest
from django.urls import reverse

from apps.baskets.models import Basket


@pytest.mark.django_db
def test_get_profile_page(client, user):
    client.force_login(user)
    url = reverse("users:profile", kwargs={"pk": user.id})
    basket = Basket.objects.get_or_create(user=user)
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["user"] == user
    assert response.context["title"] == f"Профиль пользователя: {user.username}"

@pytest.mark.django_db
def test_updates_profile_data(client, user, test_avatar):
    client.force_login(user)
    basket = Basket.objects.get_or_create(user=user)

    initial_profile = user.profile
    assert initial_profile.first_name is None

    url = reverse("users:profile-update", kwargs={"pk": user.profile.pk})
    data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "phone": "9876543210",
        "email": "new@example.com",
        "avatar": test_avatar
    }
    response = client.post(url, data, follow=True)

    user.refresh_from_db()
    user.profile.refresh_from_db()

    assert user.profile.first_name == data["first_name"]
    assert user.profile.last_name == data["last_name"]
    assert user.profile.phone == data["phone"]
    assert user.profile.email == data["email"]
    assert "test_avatar.jpg" in user.profile.avatar.name
