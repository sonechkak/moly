from django.template.defaultfilters import title
from django.test import TestCase
from django.utils.text import slugify

from apps.shop.models import Category


class CategoryTestCase(TestCase):
    """Тест для модели Category."""
    def setUp(self):
        Category.objects.create(
            title="Тестовая категория 1",
        )

    def test_category(self):
        """Тестируем создание категории."""
        category = Category.objects.get(id=1)
        self.assertEqual(category.title, "Тестовая категория 1")
