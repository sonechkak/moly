from apps.shop.models import Product
from django.conf import settings
from django.db import models

user_model = settings.AUTH_USER_MODEL


class FavoriteProducts(models.Model):
    """Класс для избранных товаров."""

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="favorite")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="favorite")

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"

    def __str__(self):
        return self.product.title
