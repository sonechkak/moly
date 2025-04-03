from datetime import timedelta

from apps.shop.models import Category, Product
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

user_model = get_user_model()


class Subscribe(models.Model):
    """Подписка."""

    email = models.EmailField()
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_general = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return self.email


class Promotion(models.Model):
    """Класс для управления акциями, скидками и специальными предложениями."""

    title = models.CharField("Название акции", max_length=100)
    message = models.TextField("Описание акции")
    discount_percent = models.PositiveIntegerField("Процент (%) скидки", default=0)
    is_active = models.BooleanField("Активна", default=True)

    # Сроки проведения
    start_date = models.DateTimeField("Начало акции", default=timezone.now)
    end_date = models.DateTimeField("Конец акции")

    products = models.ManyToManyField(Product, related_name="promotions", blank=True, verbose_name="Товары по акции")

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f"{self.title}. Успейте купить товары со скидкой {self.discount_percent}%!"

    @classmethod
    def get_active_promotions(cls):
        """Получение активных акций."""
        now = timezone.now()
        return cls.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now).order_by("-start_date")
