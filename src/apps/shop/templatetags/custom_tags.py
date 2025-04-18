from apps.shop.models import Category
from django import template
from django.core.cache import caches
from django.template.defaultfilters import register as range_register

cache = caches["default"]
register = template.Library()


def calculate_average(values):
    """Вычисление среднего значения."""

    if not values:
        return 0

    total = 0
    count = 0

    for value in values:
        if isinstance(value, str):
            total += int(value)
            count += 1

    if count == 0:
        return 0

    return round(total / count)


@register.simple_tag()
def multiply(value, arg):
    """Умножение двух чисел."""

    cache_key = f"multiply_{value}_{arg}"
    result = cache.get(cache_key)

    if result is None:
        result = float(value) * float(arg)
        cache.set(cache_key, result, 60 * 15)

    return result


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
                    ("price", "по возрастанию"),
                    ("-price", "по убыванию"),
                ],
            },
            {
                "title": "Популярность",
                "sorters": [
                    ("watched", "по возрастанию"),
                    ("-watched", "по убыванию"),
                ],
            },
            {
                "title": "Цвет",
                "sorters": [
                    ("color", "от А до Я"),
                    ("-color", "от Я до А"),
                ],
            },
            {
                "title": "Размер",
                "sorters": [
                    ("size", "по возрастанию"),
                    ("-size", "по убыванию"),
                ],
            },
        ]

    return sorters


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


@range_register.filter()
def get_average_rating(values):
    """Фильтр для среднего значения."""

    cache_key = f"average_rating_{values}"
    average_rating = cache.get(cache_key)

    if average_rating is None:
        average_rating = calculate_average(values)
        cache.set(cache_key, average_rating, 60 * 15)

    return average_rating


@register.filter
def mapping(queryset, attr):
    """Фильтр для извлечения значений атрибута из QuerySet."""

    cache_key = f"mapping_{attr}"
    mapping_result = cache.get(cache_key)

    if mapping_result is None:
        mapping_result = [getattr(obj, attr) for obj in queryset]
        cache.set(cache_key, mapping_result, 60 * 15)

    return mapping_result
