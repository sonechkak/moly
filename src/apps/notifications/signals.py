from apps.loyalty.models import UserLoyalty
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


@receiver(post_save, sender=UserLoyalty)
def user_loyalty_notification(sender, instance, created, **kwargs):
    """Отправка уведомления при обновлении лояльности пользователя."""
    user = instance.user

    if instance.current_level:
        create_notification(
            user=user,
            title="Уровень лояльности изменен!",
            message=f"Поздравляем! Ваш уровень лояльности изменен на {instance.current_level.name}. "
            f"Теперь ваш кэшбэк составляет {instance.current_level.cashback_percentage}%.",
            notification_type="loyalty_level_changed",
            url="/profile/loyalty/",
        )
