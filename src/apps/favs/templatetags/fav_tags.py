from django import template

register = template.Library()


@register.simple_tag
def get_favorite_product_ids(user):
    """Возвращает set ID избранных продуктов"""
    if not user.is_authenticated:
        return set()

    return set(user.favorite.values_list("product_id", flat=True))


@register.simple_tag
def is_product_favorite(product_id, favorite_ids):
    """Проверяет, находится ли продукт в избранном"""
    return int(product_id) in favorite_ids
