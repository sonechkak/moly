import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from utils.db import TimeStamp

from .enums.referral_status import ReferralChoices

User = get_user_model()


def generate_token():
    return secrets.token_urlsafe(32)  # криптостойкий токен


class UserReferral(TimeStamp, models.Model):
    """Класс рефералов пользователей."""

    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals", verbose_name="Амбассадор")
    referred = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referred_by", verbose_name="Приглашенный"
    )
    status = models.CharField(
        max_length=1,
        choices=ReferralChoices.choices,
        default=ReferralChoices.COMPLETED,
        verbose_name="Вознаграждение выдано",
    )

    class Meta:
        unique_together = (("referrer", "referred"),)
        verbose_name = "Реферальная связь"
        verbose_name_plural = "Реферальные связи"

    def __str__(self):
        return f"Пользователь {self.referrer} пригласил {self.referred}."


class ReferralLink(models.Model):
    """Модель реферальной ссылки пользователя."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referral_links", verbose_name="Пользователь")
    token = models.CharField(default=generate_token, unique=True, verbose_name="Токен")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    expires_at = models.DateTimeField(
        default=timezone.now() + timedelta(days=7), verbose_name="Дата окончания действия"
    )
    clicks = models.PositiveIntegerField(default=0, verbose_name="Количество переходов")

    class Meta:
        verbose_name = "Реферальная ссылка"
        verbose_name_plural = "Реферальные ссылки"

    def __str__(self):
        return f"Реферальная ссылка пользователя{self.user}."

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_token()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.is_active and self.expires_at >= timezone.now()
