import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def info_created_user_profile(sender, instance, created, **kwargs):
    """Логирование при создании Order."""
    if created:
        logger.info(f"Пользователь {sender.profile} оформил заказ {instance.pk}.")
