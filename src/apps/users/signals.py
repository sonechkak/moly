import pyotp
from apps.baskets.models import Basket
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Создает профиль автоматически при создании нового пользователя."""
    if created:
        Profile.objects.create(
            user=instance,
            mfa_hash=pyotp.random_base32(),
        )


@receiver(post_save, sender=User)
def create_basket(sender, instance, created, **kwargs):
    """Создает корзину при создании Profile."""
    if created and instance.profile:
        Basket.objects.create(user=instance)
