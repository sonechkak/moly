import pytest

from apps.referral.models import UserReferral


# Тесты для ReferralLink
@pytest.mark.django_db
def test_referral_link_str(referral_link):
    assert str(referral_link) == f"Реферальная ссылка пользователя{referral_link.user}."

@pytest.mark.django_db
def test_referral_link_is_valid(referral_link):
    assert referral_link.is_valid()

@pytest.mark.django_db
def test_expired_referral_link_is_invalid(expired_referral_link):
    assert not expired_referral_link.is_valid()

@pytest.mark.django_db
def test_inactive_referral_link_is_invalid(inactive_referral_link):
    assert not inactive_referral_link.is_valid()


# Тесты для UserReferral
@pytest.mark.django_db
def test_user_referral_str(user, referral_user):
    referral = UserReferral.objects.create(referrer=referral_user, referred=user)
    assert str(referral) == f"Пользователь {referral_user.username} пригласил {user.username}."

@pytest.mark.django_db
def test_unique_referral_constraint(user, referral_user):
    UserReferral.objects.create(referrer=referral_user, referred=user)
    with pytest.raises(Exception):
        UserReferral.objects.create(referrer=referral_user, referred=user)
