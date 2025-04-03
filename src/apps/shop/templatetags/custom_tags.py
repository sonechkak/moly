from django import template
from django.template.defaultfilters import register as range_register

from ..models import Category, Review

register = template.Library()


@register.simple_tag()
def get_subcategories(category):
    """Получение подкатегорий."""
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
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
    return range(int(value))


@range_register.filter()
def get_negative_range(value):
    """Фильтр для негативных чисел."""
    max_rate = 5
    return range(max_rate - int(value))


@range_register.filter()
def get_val(value):
    """Фильтр для негативных чисел."""
    return range(value)


@range_register.filter()
def get_average_rating(values):
    """Фильтр для среднего значения."""
    if not values:
        return 0

    total = 0
    count = 0

    for value in values:
        if isinstance(value, str):
            total += int(value)
            count += 1

    print(count, total)

    if count == 0:
        return 0

    return round(total / count)


@register.filter
def map(queryset, attr):
    """Фильтр для извлечения значений атрибута из QuerySet."""
    return [getattr(obj, attr) for obj in queryset]
