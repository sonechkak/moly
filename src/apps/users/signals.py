from apps.baskets.models import Basket
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=Profile)
def create_basket(sender, instance, created, **kwargs):
    """Создает корзину при создании Profile."""
    if created:
        user = get_user_model().objects.get(pk=instance.pk)
        Basket.objects.create(user=user)
