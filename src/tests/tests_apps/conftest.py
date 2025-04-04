import pytest
from django.contrib.auth import get_user_model

from apps.baskets.models import Basket, BasketProduct
from apps.favs.models import FavoriteProducts
from apps.shop.models import (
    Product,
    Category,
    Brand,
    Review,
    Gallery
)


@pytest.fixture
def user(transactional_db):
    user = get_user_model()
    user = user.objects.create(username="test_user")
    user.set_password("StrongPassword123!")
    user.save()
    return user

@pytest.fixture
def category(transactional_db):
    category = Category.objects.create(
        title="test_category",
        slug="test_category",
    )
    return category

@pytest.fixture
def brand(transactional_db):
    brand = Brand.objects.create(
        title="Apple",
        image="test_image",
        slug="apple",
    )
    return brand

@pytest.fixture
def product(transactional_db):
    return Product.objects.create(
        title="Тестовый товар",
        price=100,
        watched=0,
        quantity=10,
        description="Описание",
        info="Информация",
        size=30,
        color="Красный",
        slug="test-product",
    )

@pytest.fixture
def basket_with_product(transactional_db, user, product):
    basket, _ = Basket.objects.get_or_create(user=user)
    basket_product = BasketProduct.objects.create(basket=basket, product=product, quantity=1)
    return basket

@pytest.fixture
def basket_with_products(transactional_db, user, product):
    basket, _ = Basket.objects.get_or_create(user=user)
    products = []
    for i in range(3):
        p = Product.objects.create(
            title=f"Товар {i}",
            price=100 + i,
            watched=0,
            quantity=10,
            description="Описание",
            info="Информация",
            size=30,
            color="Красный"
        )
        products.append(p)
        BasketProduct.objects.create(basket=basket, product=p, quantity=i+1)
    return basket

@pytest.fixture
def favs_with_products(transactional_db, user):
    products = []
    for i in range(3):
        p = Product.objects.create(
            title=f"Любимый товар {i}",
            price=100 + i,
            watched=0,
            quantity=10,
            description="Описание",
            info="Информация",
            size=30,
            color="Красный"
        )
        products.append(p)
        FavoriteProducts.objects.create(user=user, product=p)
    return products

@pytest.fixture
def favs_without_product(transactional_db, user):
    favs, _ = Basket.objects.get_or_create(user=user)
    return favs
