import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Subscribe

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Subscribe)
def info_created_subscribe(sender, instance, created, **kwargs):
    """Логирование при создании Subscribe."""
    if created:
        try:
            user = instance.user
            logger.info(
                f"Пользователь {user.username} создал подписку #{instance.pk}",
                extra={
                    "user_id": user.id,
                    "action": "create_subscribe",
                },
            )
        except AttributeError:
            pass
