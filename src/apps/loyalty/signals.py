from apps.orders.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserLoyalty
from .services.loyalty_service import LoyaltyService


@receiver(post_save, sender=Order)
def process_order_loyalty(sender, instance, created, **kwargs):
    """Обрабатывает лояльность после сохранения заказа."""

    if created:
        if instance.is_paid and instance.user:
            LoyaltyService.process_order_cashback(instance)
