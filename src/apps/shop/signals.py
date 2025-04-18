from django.core.cache import caches
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import Category, Product, Review

cache = caches["default"]


def clear_products_cache():
    """Очищает все кэши, связанные с товарами"""
    cache.delete_many(["top_products", "top_3_products_by_reviews", "subcategories_page_products"])


def clear_categories_cache():
    """Очищает все кэши, связанные с категориями"""
    cache.delete_many(["parent_categories", "filter_sorters"])


@receiver([post_save, post_delete], sender=Product)
def product_cache_invalidate(sender, instance, **kwargs):
    """Сигнал для очистки кэша при изменении товара."""
    clear_products_cache()
    cache.delete(f"product_{instance.slug}")
    cache.delete_pattern("similar_products_*")


@receiver([post_save, post_delete], sender=Category)
def category_cache_invalidate(sender, instance, **kwargs):
    """Сигнал для очистки кэша при изменении категории."""
    clear_categories_cache()
    cache.delete_pattern("subcategories_*")


@receiver(m2m_changed, sender=Product.category.through)
def product_category_changed(sender, instance, **kwargs):
    """Сигнал для очистки кэша при изменении категории товара."""
    clear_products_cache()
    clear_categories_cache()
    cache.delete(f"product_{instance.slug}")
