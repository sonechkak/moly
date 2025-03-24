from django.contrib.auth import get_user_model
from django.db import models

from apps.shop.models import Product
from utils.db import TimeStamp

user_model = get_user_model()


class Basket(TimeStamp, models.Model):
    """Корзина с товарами."""
    user = models.OneToOneField(
        user_model,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="basket",
        verbose_name="Пользователь"
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class BasketProduct(TimeStamp, models.Model):
    """Привязка продукта к корзине, артикул товара."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="ordered_n")
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total_price(self):
        """Для получения стоимости."""
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"
