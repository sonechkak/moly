import logging

from apps.favs.models import FavoriteProducts
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=FavoriteProducts)
def info_fav_product_created(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о добавлении товара в избранное."""
    if created:
        logger.info(
            f"Пользователь {instance.user} добавил в избранное {instance.product}.",
            extra={"user_id": instance.user.pk, "action": "add_favorite"},
        )


@receiver(post_delete, sender=FavoriteProducts)
def info_fav_product_deleted(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации об удалении продукта из избранного."""
    if created:
        logger.info(
            f"Пользователь {instance.user} удалил из избранного {instance.product}.",
            extra={
                "user_id": instance.user.pk,
                "action": "from_favorite",
            },
        )
