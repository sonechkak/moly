from django.db import models
from django.utils.translation import gettext_lazy as _


class CashbackTypeChoices(models.TextChoices):
    """Класс для выбора типа кэшбэка."""

    BIRTHDAY = "birthday", _("День рождения")
    REFERRAL = "referral", _("Реферальный")
    PURCHASE = "purchase", _("Покупка")
    PROMOTION = "promotion", _("Акция")
    OTHER = "other", _("Прочее")
