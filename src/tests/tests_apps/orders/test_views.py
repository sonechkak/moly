import pytest
from django.urls import reverse

from apps.baskets.models import BasketProduct


@pytest.mark.django_db
def test_checkout(client, user, basket_with_products):
    client.force_login(user)

    url = reverse("orders:checkout", kwargs={"pk": basket_with_products.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["title"] == "Оформление заказа"
    basket_products = BasketProduct.objects.filter(basket=basket_with_products)
    assert response.context["basket_products"].count() == basket_products.count()
    assert response.context["form"] is not None


@pytest.mark.django_db
def test_order_detail(client, user, order):
    client.force_login(user)
    url = reverse("orders:order_detail", kwargs={"pk": order.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["title"] == f"Детали заказа: {order.id}"
    assert response.context["order"] == order
