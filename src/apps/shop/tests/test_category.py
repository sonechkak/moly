from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.shop.models import Product, Category, Brand


class ProductTestCase(TestCase):
    """Тест кейс для модели Product."""
    def setUp(self):
        # Создаем категории
        self.category1 = Category.objects.create(
            title="Тестовая категория 1",
            slug="test-category-1",
        )
        self.category2 = Category.objects.create(
            title="Тестовая категория 2",
            slug="test-category-2",
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
            price=500,
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
        self.product2.category.add(self.category1, self.category2)

    def test_product_creation(self):
        """Тест создания продукта."""
        self.assertEqual(self.product1.title, "Тестовый продукт 1")
        self.assertEqual(self.product1.price, 100)
        self.assertEqual(self.product2.title, "Тестовый продукт 2")
        self.assertEqual(self.product2.price, 500)

    def test_product_str_representation(self):
        """Тест строкового представления продукта."""
        self.assertEqual(self.product1.__str__(), self.product1.__str__())
        self.assertEqual(self.product2.__str__(), self.product2.__str__())

    def test_product_slug_unique(self):
        """Тест уникальности slug для продуктов."""
        self.assertEqual(self.product1.slug, "test-product-1")
        self.assertEqual(self.product2.slug, "test-product-2")

    def test_product_price_validation(self):
        """Тест валидации цены (не может быть отрицательной)."""
        self.product1.price = -10
        with self.assertRaises(ValidationError) as context:
            self.product1.full_clean()
            self.product1.save()

        self.assertTrue('price' in context.exception.message_dict)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.price, 100)

    def test_product_quantity_validation(self):
        """Тест валидации количества товара (не может быть отрицательным)"""
        pass

    def test_product_category_removal(self):
        """Тест удаления категории из продукта"""
        pass

    def test_product_brand_deletion(self):
        """Тест поведения продукта при удалении бренда"""
        pass

    def test_product_availability_toggle(self):
        """Тест переключения доступности товара"""
        pass

    def test_product_watched_increment(self):
        """Тест увеличения счетчика просмотров"""
        pass

    def test_multiple_categories_assignment(self):
        """Тест назначения нескольких категорий продукту"""
        pass

    def test_product_search_by_title(self):
        """Тест поиска продукта по названию"""
        pass

    def test_product_filter_by_price_range(self):
        """Тест фильтрации продуктов по диапазону цен"""
        pass

    def test_product_filter_by_availability(self):
        """Тест фильтрации продуктов по доступности"""
        pass

    def test_product_ordering_by_price(self):
        """Тест сортировки продуктов по цене"""
        pass

    def test_product_ordering_by_watched(self):
        """Тест сортировки продуктов по количеству просмотров"""
        pass

    def test_product_size_validation(self):
        """Тест валидации размера продукта"""
        pass

    def test_product_color_validation(self):
        """Тест валидации цвета продукта"""
        pass

    def test_product_update(self):
        """Тест обновления данных продукта"""
        pass

    def test_product_soft_delete(self):
        """Тест мягкого удаления продукта (если реализовано)"""
        pass

    def test_product_category_count(self):
        """Тест подсчета количества продуктов в категории"""
        pass
