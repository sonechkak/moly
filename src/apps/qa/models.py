from apps.shop.models import Product
from django.contrib.auth import get_user_model
from django.db import models
from utils.db import TimeStamp

User = get_user_model()


class Question(TimeStamp, models.Model):
    """Класс модели вопроса пользователя."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"Пользователь {self.user} задал вопрос о товаре: {self.product}: '{self.text}'."


class Answer(TimeStamp, models.Model):
    """Класс модели ответа магазина на вопрос."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers", null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="answers")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"Ответ на вопрос: {self.question.pk}: '{self.text}'."
