from apps.shop.models import Product
from django.contrib.auth import get_user_model
from django.db import models
from utils.db import TimeStamp

user_model = get_user_model()


class Basket(TimeStamp, models.Model):
    """Корзина с товарами."""

    user = models.OneToOneField(
        user_model, on_delete=models.CASCADE, primary_key=True, related_name="basket", verbose_name="Пользователь"
    )
    recipient = models.CharField("Получатель", max_length=255, blank=True, null=True)
    contact = models.CharField("Контакты", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.pk)

    @property
    def get_total_cost(self):
        """Для получения общей стоимости товаров в корзине."""
        prices = [product.get_total_price for product in self.ordered_n.all()]
        quantities = [product.quantity for product in self.ordered_n.all()]
        total_cost = sum([price * quantity for price, quantity in zip(prices, quantities, strict=False)])
        return total_cost

    @property
    def get_total_quantity(self):
        """Для получения количества товаров в корзине."""
        products = sum([product.quantity for product in self.ordered_n.all()])
        return products


class BasketProduct(TimeStamp, models.Model):
    """Привязка продукта к корзине, артикул товара."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="ordered_n")
    quantity = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"

    def __str__(self):
        return self.product.title

    @property
    def get_total_price(self):
        """Для получения стоимости товаров в корзине."""
        return self.product.price * self.quantity
