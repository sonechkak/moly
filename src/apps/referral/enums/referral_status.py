from django.db import models
from django.utils.translation import gettext_lazy as _


class ReferralChoices(models.TextChoices):
    """Класс для выбора статуса реферальной программы."""

    PENDING = "P", _("В ожидании")
    COMPLETED = "C", _("Завершено")
    REJECTED = "R", _("Отклонено")
