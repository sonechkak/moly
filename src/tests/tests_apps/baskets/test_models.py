import pytest

from apps.baskets.models import Basket


@pytest.mark.django_db
def test_basket_creation(user, basket_with_products):
    """Проверка создания корзины."""
    assert basket_with_products.user == user
    assert basket_with_products.pk == Basket.objects.get(user=user).pk


@pytest.mark.django_db
def test_basket_model(user, basket_with_products):
    """Тест модели корзины."""
    basket = Basket.objects.get(user=user)

    assert basket.pk is not None
    assert str(basket) == str(basket_with_products.pk)
    assert basket.get_total_cost == basket_with_products.get_total_cost
    assert basket.get_total_quantity == basket_with_products.get_total_quantity
