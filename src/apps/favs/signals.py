import logging

from apps.favs.models import FavoriteProducts
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=FavoriteProducts)
def info_created_new_review(sender, instance, created, **kwargs):
    """Логирование добавления продукта в FavoriteProducts."""
    if created:
        logger.info(
            f"Пользователь {instance.user} добавил в избранное {instance.product}",
            extra={"user_id": instance.user.pk, "action": "add_to_favorites", "user_action": True},
        )
