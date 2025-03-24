from django.contrib.auth import get_user_model
from django.db import models

from apps.shop.models import Product

user_model = get_user_model()

class FavoriteProducts(models.Model):
    """Класс для избранных товаров."""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="favorite")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="favorite")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
