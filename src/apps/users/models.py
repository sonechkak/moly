from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import get_avatar_upload_path


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField("Username", unique=True, max_length=255, null=True, blank=True)
    first_name = None
    last_name = None


class Profile(models.Model):
    """Модель профиля пользователя."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    first_name = models.CharField("first name", max_length=150, blank=True, null=True)
    last_name = models.CharField("last name", max_length=150, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to=get_avatar_upload_path, null=True, blank=True)
    email = models.EmailField("email address", blank=True, null=True)
    phone = models.CharField("phone", max_length=20, blank=True, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.user.username or self.user.email


class ShippingAddress(models.Model):
    """Адреса доставки."""

    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="address", null=True)
    title = models.TextField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    street = models.CharField(max_length=80)
    house = models.CharField(max_length=6)
    apartment = models.CharField(max_length=6, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    recipient = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    is_save_address = models.BooleanField(default=True)
    zipcode = models.TextField("Почтовый индекс", max_length=8, null=True, blank=True)

    class Meta:
        verbose_name = "Адрес доставки"
        verbose_name_plural = "Адреса доставки"

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}, {self.apartment}"
