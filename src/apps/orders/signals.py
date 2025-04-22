import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=Order)
def info_created_order(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о создании заказа."""
    if created:
        logger.info(
            f"Пользователь {instance.customer} создал заказ #{instance.pk}.",
            extra={
                "user_id": instance.customer.pk,
                "action": "create_order",
                "order_id": instance.pk,
                "order_total": instance.total_cost,
                "order_status": instance.payment_status,
            },
        )
