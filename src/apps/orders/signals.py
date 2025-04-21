import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def info_created_user_profile(sender, instance, created, **kwargs):
    """Логирование при создании Order."""
    if created:
        user = getattr(instance.customer, "user", None)
        logger.info(
            f"Пользователь {user} создал заказ #{instance.pk}",
            extra={
                "user_id": user.id,
                "action": "create_order",
            },
        )
