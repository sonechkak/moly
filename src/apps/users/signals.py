import logging

from apps.baskets.models import Basket
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()

logger = logging.getLogger(__name__)


@receiver(post_save, sender=[User, Profile])
def info_created_user_profile(sender, instance, created, **kwargs):
    """Логирование при создании User и Profile."""
    if created:
        logger.info(f"Создан пользователь {instance.username} с ID {instance.pk}")
        logger.info(f"Создан профиль {instance} с ID {instance.pk}")


@receiver(post_save, sender=Profile)
def create_basket(sender, instance, created, **kwargs):
    """Создание корзины при создании Profile и логирование."""
    if created:
        user = get_user_model().objects.get(pk=instance.pk)
        Basket.objects.create(user=user)
        logger.info(f"Корзина создана для пользователя {user.username} с ID {user.id}")
