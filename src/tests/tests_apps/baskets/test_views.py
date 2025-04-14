import pytest
from django.urls import reverse

from apps.baskets.models import BasketProduct


@pytest.mark.django_db
def test_basket_view(client, user, basket_with_products):
    """Тест страницы корзины."""
    client.force_login(user)
    url = reverse("baskets:basket", kwargs={"pk": basket_with_products.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data["basket"] == basket_with_products
    assert response.context_data["title"] == "Корзина"


@pytest.mark.django_db
def test_add_to_basket(client, user, product):
    """Тест добавления товара в корзину."""
    client.force_login(user)

    basket_url = reverse("baskets:to_basket", kwargs={"pk": product.pk})
    referer_url = 'http://localhost/products/'
    response = client.get(basket_url, HTTP_REFERER=referer_url)

    assert response.status_code == 302
    assert response.url == referer_url
    assert BasketProduct.objects.filter(basket=user.basket, product=product).exists()


@pytest.mark.django_db
def test_remove_from_basket(client, user, basket_with_product):
    """Тест удаления товара из корзины."""
    client.force_login(user)

    product = BasketProduct.objects.get(basket=basket_with_product.pk)
    url = reverse("baskets:from_basket", kwargs={"pk": product.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert not BasketProduct.objects.filter(pk=product.pk).exists()
