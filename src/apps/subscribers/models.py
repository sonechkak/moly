from django.contrib.auth import get_user_model
from django.db import models

from apps.shop.models import Product, Category


user_model = get_user_model()


class Subscribe(models.Model):
    """Подписка."""
    email = models.EmailField()
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_general = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
