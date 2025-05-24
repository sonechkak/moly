from decimal import Decimal

from apps.orders.models import Order
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from utils.db import TimeStamp

from .enums.cashback_choices import CashbackChoices
from .enums.cashback_types import CashbackTypeChoices

User = get_user_model()


class Cashback(TimeStamp, models.Model):
    """Модель кэшбэка."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cashback", verbose_name="Пользователь")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="cashback", verbose_name="Заказ", null=True, blank=True
    )
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма кэшбэка")
    cashback_status = models.CharField(
        max_length=255,
        choices=CashbackChoices.choices,
        default=CashbackChoices.PENDING,
        verbose_name="Статус кэшбэка",
    )
    type = models.CharField(
        max_length=255,
        choices=CashbackTypeChoices.choices,
        default=CashbackTypeChoices.PURCHASE,
        verbose_name="Тип кэшбэка",
    )
    expiry_date = models.DateTimeField("Дата истечения срока действия", default=timezone.now() + timedelta(days=30))
    is_expired = models.BooleanField("Истек ли срок", default=False)

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
    last_expiry_check = models.DateTimeField("Последняя проверка истечения", auto_now=True)

    class Meta:
        verbose_name = "Баланс кэшбэка"
        verbose_name_plural = "Балансы кэшбэка"

    def __str__(self):
        return str(self.total)

    def save(self, *args, **kwargs):
        """При сохранении проверяем просроченный кэшбэк."""
        self.check_expired_cashback()
        super().save(*args, **kwargs)

    def check_expired_cashback(self):
        """Проверяет и обрабатывает просроченный кэшбэк."""

        expired_cashbacks = Cashback.objects.filter(user=self.user, expiry_date__lte=timezone.now(), is_expired=False)

        total_expired = expired_cashbacks.aggregate(total=models.Sum("amount"))["total"] or 0

        if total_expired > 0:
            # Помечаем кэшбэки как просроченные
            expired_cashbacks.update(is_expired=True)

            # Обновляем баланс
            self.total = max(0, self.total - total_expired)
            self.save()
