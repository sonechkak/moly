import random
import string
from datetime import timedelta

from apps.coupons.models import Coupon
from django.utils import timezone


def generate_coupon_code(length=10, digits=False):
    """Генерация уникального кода купона."""

    if digits:
        characters = string.digits
    else:
        characters = string.ascii_uppercase + string.digits

    coupon_code = "".join(random.choice(characters) for _ in range(length))
    return coupon_code


def generate_coupon(user, days, discount):
    """Генерация купона для реферальной ссылки."""

    coupon = Coupon.objects.create(
        code=generate_coupon_code(),
        user=user,
        valid_from=timezone.now(),
        valid_to=timezone.now() + timedelta(days=days),
        discount=discount,
    )
    return coupon
