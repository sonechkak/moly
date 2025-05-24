from apps.cashback.models import Cashback
from apps.cashback.utils.create_cashback import create_cashback
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def check_birthdays():
    """Проверка пользователей с днем рождения и начисление кэшбэка."""

    today = timezone.now().date()
    users = User.objects.filter(birth_date__month=today.month, birth_date__day=today.day)

    for user in users:
        create_cashback(user=user, birthday_bonus=True, amount=1000)
