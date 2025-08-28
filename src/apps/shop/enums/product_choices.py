from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductCPUChoices(models.TextChoices):
    """Класс для выбора размера CPU."""

    M1 = "M1", _("M1")
    M2 = "M2", _("M2")
    M3 = "M3", _("M3")
    M4 = "M4", _("M4")
    Intel = "Intel", _("Intel")


class ProductRamChoices(models.TextChoices):
    """Класс для выбора размера оперативной памяти."""

    MINIMAL = "8GB", _("8GB")
    STANDARD = "16GB", _("16GB")
    LIGHT = "24GB", _("24GB")
    MEDIUM = "32GB", _("32GB")
    LARGE = "64GB", _("64GB")


class ProductStorageChoices(models.TextChoices):
    """Класс для выбора размера накопителя."""

    STANDARD = "64GB", _("64GB")
    NORMAl = "128GB", _("128GB")
    MEDIUM = "256GB", _("256GB")
    LARGE = "512GB", _("512GB")
    MAX = "1T", _("1TB")
