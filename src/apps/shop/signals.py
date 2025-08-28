import logging

from apps.notifications.models import ProductAvalaibilityNotification
from apps.notifications.services.create_notification import create_notification
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product, Review

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=Review)
def info_new_review_created(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о создании отзыва."""
    if created:
        logger.info(
            f"Пользователь {instance.author} опубликовал отзыв для товара {instance.product}.",
            extra={
                "user_id": instance.author.pk,
                "action": "add_review",
            },
        )


@receiver(post_delete, sender=Review)
def info_review_deleted(sender, instance, **kwargs):
    """Сигнал для добавления в лог информации об удалении отзыва."""
    logger.info(
        f"Пользователь {instance.author} удалил комментарий для товара {instance.product}.",
        extra={
            "user_id": instance.author,
            "action": "remove_review",
        },
    )


@receiver(post_save, sender=Product)
def handle_product_availability_notification(sender, instance, **kwargs):
    """Сигнал для обработки уведомлений о доступности товара."""

    if instance.available and instance.quantity > 0:
        # Получаем все уведомления о доступности товара
        notifications = ProductAvalaibilityNotification.objects.filter(
            product=instance,
            notified=False,
        )
        for notification in notifications:
            create_notification(
                user=notification.user,
                title="Товар доступен для заказа!",
                message=f"Товар {instance.title} теперь доступен для заказа.",
                notification_type="product_available",
                url=instance.get_absolute_url(),
            )
            notification.notified = True
            notification.save(update_fields=["notified"])

            logger.info(
                f"Уведомление о доступности товара {instance.product} отправлено пользователю {notification.user}.",
                extra={
                    "user_id": notification.user.pk,
                    "action": "product_availability_notification",
                },
            )
