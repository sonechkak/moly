from django import template
from ..models import Category

register = template.Library()

@register.simple_tag()
def get_subcategories(category):
    """Получение подкатегорий."""
    return Category.objects.filter(parent=category)

@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Цена',
            'sorters': [
                ('price', 'по возрастанию'),
                ('-price', 'по убыванию'),
            ]
        },
        {
            'title': 'Популярность',
            'sorters': [
                ('watched', 'по возрастанию'),
                ('-watched', 'по убыванию'),
            ]
        },
        {
            'title': 'Цвет',
            'sorters': [
                ('color', 'от А до Я'),
                ('-color', 'от Я до А'),
            ]
        },
        {
            'title': 'Размер',
            'sorters': [
                ('size', 'по возрастанию'),
                ('-size', 'по убыванию'),
            ]
        },
    ]
    return sorters

