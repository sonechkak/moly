import logging

from apps.coupons.utils.generate import generate_coupon
from apps.referral.models import ReferralLink, UserReferral
from django.contrib import messages
from django.utils import timezone

logger = logging.getLogger("user.actions")


def process_referrals(request, referral_token, user, days, discount):
    """Обработчик реферальных пользователей."""

    try:
        referral_link = ReferralLink.objects.get(token=referral_token, is_active=True, expires_at__gte=timezone.now())
        referral = UserReferral.objects.create(
            referrer=referral_link.user,
            referred=user,
        )
        generate_coupon(user=referral.referrer, days=days, discount=discount)
        del request.session["referral_token"]

        messages.success(request, f"Вы зарегистрированы по реферальной ссылке от {referral_link.user}")
        logger.info(f"Новый реферал от пользователя {referral_link.user} -> {user.username}")
    except ReferralLink.DoesNotExist:
        messages.error(request, "Реферальная ссылка не действительна.")
    except UserReferral.DoesNotExist:
        messages.error(request, "Ошибка при обработке реферала.")
    except UserReferral.MultipleObjectsReturned:
        messages.error(request, "Вы уже зарегистрированы по этой реферальной ссылке.")
