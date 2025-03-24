from django import template

from ..models import FavoriteProducts


register = template.Library()


@register.simple_tag()
def get_favorite_products(user):
    """Вывод избранных товаров на страницы."""
    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products
