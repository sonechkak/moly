import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Basket, BasketProduct

logger = logging.getLogger("user.actions")


@receiver(post_save, sender=Basket)
def info_basket_created(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о создании корзины."""
    if created:
        logger.info(
            f"Корзина для пользователя {instance.user} создана.",
            extra={
                "user_id": instance.user.pk,
                "action": "create_basket",
                "user_action": True,
            },
        )


@receiver(post_save, sender=BasketProduct)
def info_basket_product_created(sender, instance, created, **kwargs):
    """Сигнал для добавления в лог информации о добавлении продукта в корзину."""
    if created:
        logger.info(
            f"Пользователь {instance.basket.user} добавил товар {instance} в корзину.",
            extra={
                "user_id": instance.basket.user.pk,
                "action": "add_to_basket",
                "user_action": True,
            },
        )


@receiver(post_delete, sender=BasketProduct)
def info_basket_product_deleted(sender, instance, **kwargs):
    """Сигнал для добавления в лог информации об удалении товара из корзины."""
    logger.info(
        f"Пользователь {instance.basket.user} удалил товар {instance} из корзины.",
        extra={
            "user_id": instance.basket.user.pk,
            "action": "delete_from_basket",
            "user_action": True,
        },
    )
