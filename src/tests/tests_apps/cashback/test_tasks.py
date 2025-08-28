import pytest
from django.contrib.messages import get_messages

from apps.cashback.enums.cashback_choices import CashbackChoices
from apps.cashback.enums.cashback_types import CashbackTypeChoices
from apps.cashback.models import Cashback, CashbackBalance
from apps.cashback.utils.create_cashback import create_cashback


@pytest.mark.django_db
def test_create_cashback_for_order(user, order, rf):
    """Проверяет, что кешбек создается при оформлении заказа."""
    request = rf.get('/')
    request.user = user

    create_cashback(request, user, order=order)

    # Проверяем, что кешбек создан
    cashback = Cashback.objects.filter(user=user, order=order).first()
    assert cashback is not None
    assert cashback.amount == int(order.total_cost * 0.01)
    assert cashback.cashback_status == CashbackChoices.APPROVED

    # Проверяем, что баланс обновлен
    balance = CashbackBalance.objects.get(user=user)
    assert balance.total == cashback.amount
    assert balance.total_cashback_earned == cashback.amount


@pytest.mark.django_db
def test_create_birthday_cashback_custom_amount(user, rf):
    """Проверяет, что бонус за ДР создается с указанной суммой."""
    request = rf.get('/')
    request.user = user

    custom_amount = 1500
    create_cashback(request, user, birthday_bonus=True, amount=custom_amount)

    cashback = Cashback.objects.filter(user=user, type=CashbackTypeChoices.BIRTHDAY).first()
    assert cashback.amount == custom_amount
    assert cashback.cashback_status == CashbackChoices.APPROVED

    balance = CashbackBalance.objects.get(user=user)
    assert balance.total == custom_amount


@pytest.mark.django_db
def test_create_birthday_cashback_default_amount(user, rf):
    """Проверяет, что бонус за ДР создается с суммой по умолчанию."""

    request = rf.get('/')
    request.user = user

    create_cashback(request, user, birthday_bonus=True)

    cashback = Cashback.objects.filter(user=user, type=CashbackTypeChoices.BIRTHDAY).first()
    assert cashback.amount == 1000
