import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Subscribe

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=Subscribe)
def info_created_subscribe(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о создании подписки."""
    if created:
        if instance.user:
            logger.info(
                f"Пользователь {instance.user} создал подписку #{instance.pk}.",
                extra={
                    "user_id": instance.user.id,
                    "action": "subscribe",
                },
            )
        else:
            logger.info(f"E-mail {instance.email} создал подписку #{instance.pk}.", extra={"action": "subscribe"})
