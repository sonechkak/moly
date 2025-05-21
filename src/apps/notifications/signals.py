from apps.orders.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services.create_notification import create_notification


@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    """Отправка уведомления при создании заказа."""
    user = instance.customer.user

    if created:
        create_notification(
            user=user,
            title="Новый заказ",
            message=f"Ваш заказ #{instance.id} успешно создан",
            notification_type="order",
            url=f"/all_orders/{user.id}/",
        )
    elif instance.status_changed:
        create_notification(
            user=instance.user,
            title="Статус заказа изменен",
            message=f'Статус вашего заказа #{instance.id} изменен на "{instance.get_status_display()}"',
            notification_type="order",
            url=f"/all_orders/{user.id}/",
        )
