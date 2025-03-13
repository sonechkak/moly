from django import template
from ..models import Category

register = template.Library()

@register.simple_tag()
def get_subcategories(category):
    """Получение подкатегорий."""
    return Category.objects.filter(parent=category)

