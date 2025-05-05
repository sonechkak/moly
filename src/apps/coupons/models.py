from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Coupon(models.Model):
    """Модель для промокодов."""

    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="coupons",
        null=True,
        blank=True,
        verbose_name="Персональный промокод",
    )
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"

    def __str__(self):
        return self.code

    def is_valid(self):
        """Проверка валидности."""
        now = timezone.now().date()
        return self.is_active and self.valid_from <= now <= self.valid_to
