import logging
from decimal import Decimal

from apps.cashback.models import Cashback, CashbackBalance
from django.contrib.auth import get_user_model
from django.db import models

from .utils.get_loyalty_level_icon_path import get_loyalty_level_icon_path

User = get_user_model()
logger = logging.getLogger("user.actions")


class LoyaltyLevel(models.Model):
    """Класс для модели уровня лояльности."""

    name = models.CharField("Название уровня", max_length=255)
    slug = models.SlugField("Идентификатор", max_length=255, unique=True)
    cashback_percentage = models.IntegerField("Процент кэшбэка", default=0)
    min_points = models.PositiveIntegerField("Минимальное количество баллов")
    max_points = models.PositiveIntegerField("Максимальное количество баллов")
    icon = models.ImageField("Значок уровня", upload_to=get_loyalty_level_icon_path, blank=True, null=True)
    description = models.TextField("Описание уровня", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок отображения", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Уровень лояльности"
        verbose_name_plural = "Уровни лояльности"

    def __str__(self):
        return f"{self.name} ({self.cashback_percentage}%)"


class Privilege(models.Model):
    """Класс для модели привилегии уровня лояльности."""

    name = models.CharField("Название привилегии", max_length=255)
    loyalty_level = models.ManyToManyField(LoyaltyLevel, related_name="privileges", verbose_name="Уровень лояльности")
    description = models.TextField("Описание привилегии", blank=True, null=True)

    class Meta:
        verbose_name = "Привилегия"
        verbose_name_plural = "Привилегии"

    def __str__(self):
        return self.name


class UserLoyalty(models.Model):
    """Класс для модели уровня лояльности пользователя."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="loyalty", verbose_name="Пользователь")
    current_level = models.ForeignKey(
        LoyaltyLevel,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
        verbose_name="Текущий уровень лояльности",
    )
    total_spent = models.PositiveIntegerField(
        "Общая сумма покупок",
        default=0,
    )
    cashback = models.OneToOneField(CashbackBalance, on_delete=models.CASCADE, related_name="loyalty")
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Уровень лояльности пользователя"
        verbose_name_plural = "Уровни лояльности пользователей"

    def __str__(self):
        return f"{self.user.username} - {self.current_level.name if self.current_level else "Нет уровня"}"

    def get_cashback(self):
        """Возвращает кэшбэк пользователя."""
        return self.cashback.total if self.cashback else Decimal("0.00")

    def update_level(self):
        """Обновляет уровень лояльности пользователя на основе его общей суммы покупок."""
        try:
            new_level = LoyaltyLevel.objects.filter(
                min_points__lte=self.total_spent, max_points__gte=self.total_spent
            ).first()

            # Если подходящий уровень не найден, найдем самый низкий уровень
            if not new_level:
                new_level = LoyaltyLevel.objects.order_by("min_points").first()

            # Обновляем уровень
            if new_level and new_level != self.current_level:
                self.current_level = new_level
                self.save(update_fields=["current_level"])

        except LoyaltyLevel.DoesNotExist:
            logger.error(
                "Ошибка при обновлении уровня лояльности: уровень не найден.",
                extra={"user": self.user.username, "total_spent": self.total_spent},
            )

    def get_next_level(self):
        """Получает следующий уровень лояльности пользователя."""
        return LoyaltyLevel.objects.filter(order=self.current_level.order + 1).first()

    def get_remaining_amount(self):
        """Получает оставшуюся сумму до следующего уровня лояльности."""
        current_level = self.current_level

        if not current_level:
            return 0

        next_level = self.get_next_level()
        if not next_level:
            return 0

        remaining_amount = next_level.min_points - self.total_spent
        return remaining_amount
