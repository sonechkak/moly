from decimal import Decimal

from apps.orders.models import Order
from django.contrib.auth import get_user_model
from django.db import models
from utils.db import TimeStamp

from .enums.cashback_choices import CashbackChoices

User = get_user_model()


class Cashback(TimeStamp, models.Model):
    """Модель кэшбэка."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cashback", verbose_name="Пользователь")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cashback", verbose_name="Заказ")
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма кэшбэка")
    cashback_status = models.CharField(
        max_length=20,
        choices=CashbackChoices.choices,
        default=CashbackChoices.PENDING,
        verbose_name="Статус кэшбэка",
    )

    class Meta:
        verbose_name = "Кэшбэк"
        verbose_name_plural = "Кэшбэки"

    def __str__(self):
        return f"Кэшбэк для пользователя {self.user}: {self.amount}"


class CashbackBalance(TimeStamp, models.Model):
    """Модель баланса кэшбэка."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cashback_balance", verbose_name="Пользователь"
    )
    total = models.PositiveIntegerField("Доступно кэшбэка", default=0)
    total_cashback_earned = models.DecimalField(
        "Всего заработано кэшбэка", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    total_cashback_used = models.DecimalField(
        "Всего использовано кэшбэка", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:
        verbose_name = "Баланс кэшбэка"
        verbose_name_plural = "Балансы кэшбэка"

    def __str__(self):
        return str(self.total)
