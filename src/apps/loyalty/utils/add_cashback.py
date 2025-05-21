from decimal import Decimal

from apps.cashback.enums.cashback_choices import CashbackChoices
from apps.cashback.models import Cashback, CashbackBalance
from apps.loyalty.models import UserLoyalty
from apps.loyalty.services.loyalty_service import LoyaltyService
from django.db import transaction


def update_cashback_balance(request, user, order):
    """Добавляет кэшбэк пользователю после успешного заказа."""

    if not user or not order.is_paid:
        return

    with transaction.atomic():
        cashback_balance, created = CashbackBalance.objects.get_or_create(user=user)
        user_loyalty, created = UserLoyalty.objects.get_or_create(
            user=user,
            defaults={
                "cashback": cashback_balance,
            },
        )
        if created or not user_loyalty.current_level:
            user_loyalty.update_level()

        # Рассчитываем кэшбэк
        cashback_amount = LoyaltyService.calculate_cashback(
            order_amount=order.total_cost, loyalty_level=user_loyalty.current_level
        )

        if cashback_amount > 0:
            # Начисляем кэшбэк
            Cashback.objects.create(
                user=user, order=order, amount=cashback_amount, cashback_status=CashbackChoices.APPROVED
            )

            # Обновляем баланс кэшбэка
            cashback_balance.total += cashback_amount
            cashback_balance.total_cashback_earned += Decimal(cashback_amount)
            cashback_balance.save()

            # Обновляем кэшбэк в модели UserLoyalty
            user_loyalty.total_spent += order.total_cost
            user_loyalty.save(update_fields=["total_spent"])

            # Обновляем уровень лояльности
            user_loyalty.refresh_from_db()
            user_loyalty.update_level()
