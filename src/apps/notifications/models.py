from apps.shop.models import Product
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from .enums.delivery_choices import DeliveryStatus
from .enums.notification_choices import NotificationChoices

User = get_user_model()


class Notification(models.Model):
    """Класс уведомлений."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField("Заголовок", max_length=255)
    message = models.TextField("Сообщение")
    type = models.CharField("Тип уведомления", max_length=255, choices=NotificationChoices.choices)
    status = models.CharField(
        "Статус отправки", max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING
    )
    url = models.URLField("URL", max_length=255)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


class ProductAvalaibilityNotification(models.Model):
    """Класс уведомлений о поступлении товара."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_notifications", verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="notifications", verbose_name="Товар")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    notified = models.BooleanField("Пользователь уведомлен", default=False)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Уведомление о новом товаре"
        verbose_name_plural = "Уведомления о новых товарах"

    def __str__(self):
        return f"Уведомление о новом товаре: {self.product.name}"
