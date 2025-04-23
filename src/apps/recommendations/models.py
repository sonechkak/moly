from apps.shop.models import Product
from django.contrib.auth import get_user_model
from django.db import models
from utils.db import TimeStamp

User = get_user_model()


class UserPageVisit(models.Model):
    """Модель для хранения информации о том, какие страницы товаров просматривал пользователь."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    visit_count = models.PositiveIntegerField(default=1)
    first_visited = models.DateField(auto_now_add=True)
    last_visited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Посещение страницы товара"
        verbose_name_plural = "Посещения страниц товаров"
        unique_together = ("user", "product")
        ordering = ["-last_visited"]

    def __str__(self):
        return f"Пользователь {self.user_id} открыл {self.product} в {self.last_visited}"


class Similarity(TimeStamp, models.Model):
    """Модель для хранения информации о схожести между товарами."""

    product_1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_1")
    product_2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_2")
    similarity_score = models.FloatField()

    def __str__(self):
        return f"Сходство между {self.product_1} и {self.product_2}: {self.similarity_score}"
