from apps.cashback.enums.cashback_choices import CashbackChoices
from apps.cashback.enums.cashback_types import CashbackTypeChoices
from apps.cashback.models import Cashback, CashbackBalance
from django.contrib import messages
from django.db import transaction

DEFAULT_AMOUNT = 1000


def create_cashback(request, user, order=None, birthday_bonus=False, amount=None):
    """Создание кэшбэка для пользователя."""

    with transaction.atomic():
        if order:
            amount = int(order.total_cost * 0.01)
            cashback = Cashback.objects.create(
                user=user, order=order, amount=amount, cashback_status=CashbackChoices.APPROVED
            )

        if birthday_bonus and not order:
            if amount:
                cashback = Cashback.objects.create(
                    user=user,
                    amount=amount,
                    cashback_status=CashbackChoices.APPROVED,
                    type=CashbackTypeChoices.BIRTHDAY,
                )
            else:
                cashback = Cashback.objects.create(
                    user=user,
                    amount=DEFAULT_AMOUNT,
                    cashback_status=CashbackChoices.APPROVED,
                    type=CashbackTypeChoices.BIRTHDAY,
                )

        balance, created = CashbackBalance.objects.get_or_create(user=user)
        balance.total += cashback.amount
        balance.total_cashback_earned += cashback.amount
        balance.save(update_fields=["total", "total_cashback_earned"])
