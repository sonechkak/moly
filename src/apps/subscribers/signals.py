import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Subscribe

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Subscribe)
def info_created_subscribe(sender, instance, created, **kwargs):
    """Логирование при создании Subscribe."""
    if created:
        logger.info(f"Создан подписчик {instance.email} с ID {instance.pk}")
