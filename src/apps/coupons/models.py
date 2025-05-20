from apps.shop.models import Category, Product
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from utils.db import TimeStamp

from .enums.discount_choices import DiscountChoices

User = get_user_model()
MIN_SUM_ORDER = 1000


class Coupon(TimeStamp, models.Model):
    """Модель для промокодов."""

    code = models.CharField("Код промокода", max_length=10, unique=True)
    discount_type = models.CharField(
        "Тип промокода",
        choices=DiscountChoices.choices,
        max_length=20,
        default=DiscountChoices.GENERAL,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="coupons",
        null=True,
        blank=True,
        verbose_name="Персональный промокод",
    )
    valid_from = models.DateField(
        "Дата начала действия",
        validators=[MinValueValidator(timezone.now().date())],
    )
    valid_to = models.DateField(
        "Дата окончания действия",
        validators=[MinValueValidator(timezone.now().date())],
    )
    discount = models.IntegerField("Размер скидки", validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField("Активен ли промокод", default=True)
    products = models.ManyToManyField(Product, blank=True, verbose_name="Товары со скидкой")
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Категории со скидкой")
    min_order_amount = models.IntegerField(
        default=MIN_SUM_ORDER,
        verbose_name="Минимальная сумма заказа",
    )
    used_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"

    def __str__(self):
        return f"{self.code} ({self.discount}%)"

    def is_valid(self, user=None, cart=None):
        """Проверка валидности с учетом пользователя и корзины."""
        now = timezone.now().date()
        valid_period = self.is_active and self.valid_from <= now <= self.valid_to

        if self.discount_type == "personal":
            if user and self.user != user:
                return False
            if cart and self.min_order_amount > cart.get_total_with_discount_and_cashback():
                return False

        return valid_period
