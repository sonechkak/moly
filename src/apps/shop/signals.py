import logging

from apps.shop.models import Review
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

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
        f"Пользователь {instance.author} удалил комментарий {instance} для товара {instance.product}.",
        extra={
            "user_id": instance.author,
            "action": "remove_review",
        },
    )
