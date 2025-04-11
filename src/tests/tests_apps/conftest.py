import tempfile

import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404

from apps.baskets.models import *
from apps.favs.models import FavoriteProducts
from apps.orders.models import Order, OrderProduct
from apps.shop.models import *
from apps.users.models import Profile


@pytest.fixture
def valid_registration_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'ComplexPass123!',
        'password2': 'ComplexPass123!',
        'is_mfa_enabled': False
    }

@pytest.fixture
def user(transactional_db):
    user = get_user_model().objects.create(username="test_user")
    user.set_password("StrongPassword123!")
    Profile.objects.create(user=user)
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
def categories(transactional_db):
    categories = []
    for i in range(5):
        category = Category.objects.create(
            title=f"test_category_{i}",
            slug=f"test_category_{i}",
        )
        categories.append(category)
    return categories

@pytest.fixture
def brand(transactional_db):
    brand = Brand.objects.create(
        title="Apple",
        image="test_image",
        slug="apple",
    )
    return brand

@pytest.fixture
def product(transactional_db, category, brand):
    product = Product.objects.create(
        title="Тестовый товар",
        price=100,
        watched=0,
        quantity=10,
        description="Описание",
        info="Информация",
        size=30,
        color="Красный",
        slug="test-product",
        brand=brand,
    )
    product.category.set([category])
    return product

@pytest.fixture
def products(transactional_db, categories, brand):
    products = []
    for i in range(12):
        product = Product.objects.create(
            title=f"Товар {i}",
            price=100 + i,
            watched=10 + i,
            quantity=10,
            description="Описание",
            info="Информация",
            size=30,
            color="Красный",
            slug=f"test-product-{i}",
            brand=brand,
        )
        product.category.set([categories[i % len(categories)]])
        products.append(product)
    return products

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
def favorite_product(transactional_db, user, product):
    fav, _ = Basket.objects.get_or_create(user=user)
    fav_product = FavoriteProducts.objects.create(user=user, product=product)
    return fav_product

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

@pytest.fixture
def order(transactional_db, user, basket_with_products):
    order = Order.objects.create(
        customer=get_object_or_404(Profile, user=user.id),
        address="123 Main St",
        recipient="Юра Борисов",
        contact="89663068045",
        total_cost=basket_with_products.get_total_cost,
    )
    for basket_product in basket_with_products.ordered_n.all():
        OrderProduct.objects.create(
            order=order,
            product=basket_product.product,
            quantity=basket_product.quantity,
            price=basket_product.get_total_price,
        )
    return order

@pytest.fixture
def order_product(transactional_db, order, product):
    order_product = OrderProduct.objects.create(
        order=order,
        product=product,
        quantity=2,
        price=1000,
    )
    return order_product

@pytest.fixture
def avatar():
    # Create a temporary file
    image_file = tempfile.NamedTemporaryFile(suffix='.jpg')

    # Create a small PIL image and save it to the temporary file
    image = Image.new('RGB', (100, 100), color='red')
    image.save(image_file, format='JPEG')

    # Seek to the beginning of the file
    image_file.seek(0)

    # Create a SimpleUploadedFile from the temporary file
    return SimpleUploadedFile(
        "test_avatar.jpg",
        image_file.read(),
        content_type="image/jpeg"
    )
