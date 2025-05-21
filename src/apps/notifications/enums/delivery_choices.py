from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryStatus(models.TextChoices):
    """Класс для выбора статуса отправки уведомления."""

    PENDING = "pending", _("Ожидает отправки")
    SENT = "sent", _("Отправлено")
    READ = "read", _("Прочитано")
    FAILED = "failed", _("Ошибка отправки")
