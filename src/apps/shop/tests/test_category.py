from django.test import TestCase

from ..models import Category


class CategoryTestCase(TestCase):
    """Тест для модели Category."""
    def setUp(self):
        Category.objects.create()

    def test_category(self):
        """Тестируем создание категории."""
        category = Category.objects.get(id=1)
        self.assertEqual(category.name, "Тестовая категория 1")
        self.assertEqual(category.description, "Описание категории 1")
