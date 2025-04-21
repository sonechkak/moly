import logging

from apps.shop.models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Review)
def info_created_new_review(sender, instance, created, **kwargs):
    """Логирование создание отзыва."""
    if created:
        logger.info(f"Создан отзыв {instance.pk} для товара {instance.product.pk}")
