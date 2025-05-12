from apps.shop.models import Category
from django import template
from django.core.cache import caches
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from django.template.defaultfilters import register as range_register

cache = caches["default"]
register = template.Library()


@register.simple_tag()
def get_subcategories(category):
    """Получение подкатегорий."""

    if not category or not hasattr(category, "id"):
        return Category.objects.none()

    cache_key = f"subcategories_{category.id}"
    subcategories = cache.get(cache_key)

    if subcategories is None:
        subcategories = Category.objects.filter(parent=category)
        cache.set(cache_key, subcategories, 60 * 15)

    return subcategories


@register.simple_tag()
def get_sorted():
    """Получение вариантов сортировки для фильтров."""

    cache_key = "filter_sorters"
    sorters = cache.get(cache_key)

    if not sorters:
        sorters = [
            {
                "title": "Цена",
                "sorters": [
                    ("price", "Дешевле"),
                    ("-price", "Дороже"),
                ],
            },
            {
                "title": "Популярность",
                "sorters": [
                    ("watched", "По популярности"),
                ],
            },
            {
                "title": "Цвет",
                "sorters": [
                    ("color", "Цвет от А до Я"),
                    ("-color", "Цвет от Я до А"),
                ],
            },
            {
                "title": "Наличие",
                "sorters": [
                    ("available", "Только в наличии"),
                    ("-available", "Показать все"),
                ],
            },
        ]
    return sorters


@register.simple_tag()
def get_filters():
    """Фильтрация по техническим характеристикам."""
    return {
        "cpu_type": ["M1", "M2", "M3", "M4", "Intel"],
        "ram": ["8GB", "16GB", "24GB", "32GB", "64GB"],
        "storage": ["64GB", "128GB", "256GB", "512GB", "1TB"],
    }


@range_register.filter()
def get_positive_range(value):
    """Фильтр для позитивных чисел."""

    cache_key = f"positive_range_{value}"
    positive_range = cache.get(cache_key)

    if positive_range is None:
        positive_range = range(int(value))
        cache.set(cache_key, positive_range, 60 * 15)

    return range(int(value))


@range_register.filter()
def get_negative_range(value):
    """Фильтр для негативных чисел."""

    cache_key = f"negative_range_{value}"
    negative_range = cache.get(cache_key)

    if negative_range is None:
        negative_range = range(5 - int(value))
        cache.set(cache_key, negative_range, 60 * 15)

    return negative_range


@register.filter(name="get_average_rating")
def get_average_rating(reviews):
    """Фильтр для вычисления среднего рейтинга из CharField с choices."""

    if not reviews.exists():
        return 0.0

    result = reviews.annotate(grade_int=Cast("grade", IntegerField())).aggregate(avg_rating=Avg("grade_int"))

    return round(float(result["avg_rating"]), 1) if result["avg_rating"] else 0.0
