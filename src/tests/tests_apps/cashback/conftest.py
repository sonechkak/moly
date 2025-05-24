import pytest
from apps.orders.models import Order


@pytest.fixture
def order_with_cashback(user):
    return Order.objects.create(
        user=user,
        total_cost=10000,
        cashback_used=True,
        cashback_amount=500
    )

@pytest.fixture
def rf():
    from django.test import RequestFactory
    return RequestFactory()
