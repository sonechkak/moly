import pytest


@pytest.mark.django_db
def test_basket_with_products(user, favorite_product):
    assert favorite_product.user == user
