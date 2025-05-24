from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import CashbackBalance


@shared_task
def check_expiring_cashback():
    """Периодическая проверка истекающего кэшбэка."""
    yesterday = timezone.now() - timedelta(days=1)

    balances = CashbackBalance.objects.filter(last_expiry_check__lte=yesterday)

    for balance in balances:
        balance.check_expired_cashback()
