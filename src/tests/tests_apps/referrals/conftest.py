from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.referral.models import ReferralLink
from apps.users.models import Profile

User = get_user_model()


@pytest.fixture
def referral_user(transactional_db):
    """Фикстура для пользователя, который будет реферером"""
    user = User.objects.create(
        username="referrer_user",
        password="StrongPassword123!",
        email="referrer@example.com"
    )
    Profile.objects.create(user=user)
    return user


@pytest.fixture
def referral_link(referral_user):
    """Фикстура для активной реферальной ссылки"""
    return ReferralLink.objects.create(
        user=referral_user,
        expires_at=timezone.now() + timedelta(days=7)
    )


@pytest.fixture
def expired_referral_link(referral_user):
    """Фикстура для просроченной реферальной ссылки"""
    return ReferralLink.objects.create(
        user=referral_user,
        expires_at=timezone.now() - timedelta(days=1)
    )


@pytest.fixture
def inactive_referral_link(referral_user):
    """Фикстура для неактивной реферальной ссылки"""
    return ReferralLink.objects.create(
        user=referral_user,
        is_active=False,
        expires_at=timezone.now() + timedelta(days=7)
    )
