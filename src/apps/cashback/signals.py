import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cashback, CashbackBalance

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=Cashback)
def info_cashback_created(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о создании кешбэка."""
    if created:
        logger.info(
            f"Кешбэк для пользователя {instance.user} одобрен.",
            extra={
                "user_id": instance.user.pk,
                "action": "create_cashback",
            },
        )
