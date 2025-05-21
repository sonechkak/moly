from apps.cashback.enums.cashback_choices import CashbackChoices
from apps.cashback.models import Cashback, CashbackBalance
from django.contrib import messages
from django.db import transaction


def create_cashback(request, user, order):
    """Создание кэшбэка для пользователя."""

    with transaction.atomic():
        amount = int(order.total_cost * 0.01)
        cashback = Cashback.objects.create(
            user=user, order=order, amount=amount, cashback_status=CashbackChoices.APPROVED
        )
        messages.success(request, f"Кэшбек в размере {amount} скоро зачислится на ваш счет.")

        balance, created = CashbackBalance.objects.get_or_create(user=user)
        balance.total += cashback.amount
        balance.total_cashback_earned += cashback.amount
        balance.total_cashback_used += order.cashback_amount if order.cashback_used else 0
        balance.save(update_fields=["total", "total_cashback_earned", "total_cashback_used"])
