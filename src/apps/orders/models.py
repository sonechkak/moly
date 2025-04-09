from apps.shop.models import Product
from apps.users.models import Profile
from django.db import models
from utils.db import TimeStamp


class Order(TimeStamp, models.Model):
    """Модель заказа."""

    customer = models.ForeignKey(Profile, on_delete=models.RESTRICT, verbose_name="Покупатель")
    is_complete = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    recipient = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    total_cost = models.IntegerField(default=0, null=True, blank=True)
    is_save_address = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}, {self.apartment}"


class OrderProduct(models.Model):
    """Товары в заказе."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products_n")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_products_n")
    quantity = models.IntegerField(default=1)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказа"
        ordering = ("-id",)

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"
