import pytest


@pytest.mark.django_db
def test_basket_with_products(transactional_db, user, favorite_product):
    assert favorite_product.user == user
    assert favorite_product.product == product
    assert str(favorite_product) == product.title
