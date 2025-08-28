from django.db import models
from django.utils.translation import gettext_lazy as _


class CashbackChoices(models.TextChoices):
    """Класс для выбора статуса кэшбэка."""

    PENDING = "pending", _("Ожидает")
    APPROVED = "approved", _("Одобрен")
    REJECTED = "rejected", _("Отклонен")
