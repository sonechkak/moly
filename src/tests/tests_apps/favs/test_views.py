import pytest
from django.urls import reverse

from apps.baskets.models import Basket


@pytest.mark.django_db
def test_favs_detail(client, user, favs_with_products):
    client.force_login(user)
    basket = Basket.objects.get_or_create(user=user)  # для template
    url = reverse("favs:favorites")
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["title"] == "Избранные товары"
    assert response.context_data["products"] == favs_with_products


@pytest.mark.django_db
def test_add_fav(client, user, product):
    client.force_login(user)
    url = reverse("favs:add_favorite", kwargs={"slug": product.slug})
    referer = "http://localhost/user_favorites/"
    response = client.get(url, HTTP_REFERER=referer)

    assert response.status_code == 302
    assert response.url == referer
