from apps.cashback.enums.cashback_choices import CashbackChoices
from apps.cashback.models import Cashback, CashbackBalance
from django.contrib import messages
from django.db import transaction


def create_cashback(request, user, order):
    """Создание кэшбэка для пользователя."""

    with transaction.atomic():
        cashback = Cashback.objects.create(
            user=user, order=order, amount=order.total_cost * 0.1, cashback_status=CashbackChoices.APPROVED
        )
        messages.success(request, f"Кэшбек в размере {cashback.amount} скоро зачислится на ваш счет.")

        balance, created = CashbackBalance.objects.get_or_create(user=user)
        balance.total += cashback.amount
        balance.save(update_fields=["total"])
