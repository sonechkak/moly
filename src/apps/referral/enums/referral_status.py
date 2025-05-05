from django.db import models
from django.utils.translation import gettext_lazy as _


class ReferralChoices(models.TextChoices):
    PENDING = "P", _("Pending")  # В ожидании
    COMPLETED = "C", _("Завершено")  # Завершено
    REJECTED = "R", _("Отклонено")  # Отклонено
