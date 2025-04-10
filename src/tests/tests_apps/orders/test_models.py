import pytest

from apps.users.models import Profile


@pytest.mark.django_db
def test_order_creation(user, order):
    assert order.id is not None
    assert order.customer == Profile.objects.get(user=user)
    assert order.is_complete is False

def test_order_product_creation(order_product, order, product):
    """Тест создания товара в заказе"""
    assert order_product.order == order
    assert order_product.product == product
    assert order_product.quantity == 2
    assert order_product.price == 1000
