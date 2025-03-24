from django.contrib.auth import get_user_model
from django.db import models

from apps.shop.models import Product
from utils.db import TimeStamp

user_model = get_user_model()


class Basket(TimeStamp, models.Model):
    """Корзина с товарами."""
    user = models.OneToOneField(user_model, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def get_order_total_price(self):
        """Для получения суммы товаров в корзине"""
        order_products = self.ordered.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_order_total_quantity(self):
        """Для получения общего количества товаров."""
        order_products = self.ordered.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class BasketProduct(TimeStamp, models.Model):
    """Привязка продукта к корзине, артикул товара."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="ordered_n")
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.product.title

    @property
    def get_total_price(self):
        """
        Подсчитывает свою общую цену продукта
        :return:
        """
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"
