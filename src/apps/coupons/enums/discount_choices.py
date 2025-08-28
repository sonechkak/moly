from django.db import models
from django.utils.translation import gettext_lazy as _


class DiscountChoices(models.TextChoices):
    """Класс для выбора типа промокода."""

    PERSONAL = "personal", _("Персональный промокод")
    GENERAL = "general", _("Общий промокод")
    BIRTHDAY = "birthday", _("День рождения")
    PROMO = "promo", _("Промо акция")
    BIG_ORDER = "big_order", _("Скидка за крупный заказ")
    LOYALTY = "loyalty", _("Скидка за общую сумму покупок")
