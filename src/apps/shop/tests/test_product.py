from django.test import TestCase

from apps.shop.models import Product, Category, Brand


class ProductTestCase(TestCase):
    """Тест кейс для модели Product."""
    def setUp(self):
        # Создаем категории
        self.category1 = Category.objects.create(
            title="Тестовая категория 1",
            slug="test-category-1"
        )
        self.category2 = Category.objects.create(
            title="Тестовая категория 2",
            slug="test-category-2"
        )
        self.brand = Brand.objects.create(
            title="Тестовый бренд",
            slug="test-brand"
        )
        self.product1 = Product.objects.create(
            title="Тестовый продукт 1",
            price=100,
            watched=10,
            quantity=2,
            description="Описание товара 1",
            info="Информация о товаре 1",
            size=30,
            color="Красный",
            brand=self.brand,
            available=True,
            slug="test-product-1"
        )
        self.product1.category.add(self.category1, self.category2)

        self.product2 = Product.objects.create(
            title="Тестовый продукт 2",
            price=200,
            watched=100,
            quantity=10,
            description="Описание товара 2",
            info="Информация о товаре 2",
            size=40,
            color="Синий",
            brand=self.brand,
            available=True,
            slug="test-product-2"
        )
        self.product2.category.add(self.category1)

    def test_product_creation(self):
        self.assertEqual(self.product1.title, "Тестовый продукт 1")
        self.assertEqual(self.product1.price, 100)
        self.assertEqual(self.product1.category.count(), 2)
        self.assertEqual(self.product1.brand, self.brand)
