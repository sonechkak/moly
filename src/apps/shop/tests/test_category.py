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

    def test_product_creation(self):
        self.assertEqual(self.category1.title, "Тестовая категория 1")
        self.assertEqual(self.category2.title, "Тестовая категория 2")
