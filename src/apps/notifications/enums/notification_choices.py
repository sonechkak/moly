from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationChoices(models.TextChoices):
    """Класс для выбора типа уведомления."""

    ORDER = "order", _("Заказ")
    PROMO = "promo", _("Акция")
    SYSTEM = "system", _("Системное")
    PERSONAL = "personal", _("Персональное")
    COMMENT = "comment", _("Комментарий")
    PRODUCT_AVAILABLE = "product_available", _("Товар доступен")
    LOYALTY_LEVEL_CHANGED = "loyalty_level_changed", _("Изменение уровня лояльности")
