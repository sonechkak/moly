from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.referral.enums.referral_status import ReferralChoices
from apps.referral.models import ReferralLink, UserReferral

User = get_user_model()


@pytest.mark.django_db
def test_referral_link_creation(client, referral_user):
    """Тест создания реферальной ссылки."""

    client.force_login(referral_user)
    response = client.get(reverse('referral:create', kwargs={'pk': referral_user.id}))

    assert response.status_code == 200
    data = response.json()
    assert data['status'] in ['created', 'exists']
    assert 'token' in data
    assert 'referral_url' in data

    # Проверяем, что ссылка создана
    link = ReferralLink.objects.get(user=referral_user)
    assert link.token == data['token']
    assert link.is_active

@pytest.mark.django_db
def test_referral_link_redirect(client, referral_link):
    """Тест перехода по реферальной ссылке"""
    url = reverse('referral:link', kwargs={'token': referral_link.token})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('auth:register')

    assert client.session.get('referral_token') == referral_link.token

    updated_link = ReferralLink.objects.get(pk=referral_link.pk)
    assert updated_link.clicks == referral_link.clicks + 1

@pytest.mark.django_db
def test_expired_referral_link(client, expired_referral_link):
    """Тест просроченной реферальной ссылки"""
    url = reverse('referral:link', kwargs={'token': expired_referral_link.token})
    response = client.get(url)

    assert response.status_code == 404
    assert 'referral_token' not in client.session

@pytest.mark.django_db
def test_inactive_referral_link(client, inactive_referral_link):
    """Тест неактивной реферальной ссылки"""
    url = reverse('referral:link', kwargs={'token': inactive_referral_link.token})
    response = client.get(url)

    assert response.status_code == 404
    assert 'referral_token' not in client.session

@pytest.mark.django_db
def test_referral_registration(client, referral_user, referral_link, valid_registration_data):
    """Тест регистрации по реферальной ссылке"""
    # Переход по реферальной ссылке
    response = client.get(reverse('referral:link', kwargs={'token': referral_link.token}))
    assert response.status_code == 302
    assert 'referral_token' in client.session
    assert client.session['referral_token'] == referral_link.token

    # Регистрация нового пользователя
    response = client.post(reverse('auth:register'), data=valid_registration_data)
    assert response.status_code == 302
    assert User.objects.filter(username=valid_registration_data['username']).exists()

    # Проверяем создание реферальной связи
    new_user = User.objects.get(username=valid_registration_data['username'])
    assert UserReferral.objects.filter(referrer=referral_link.user, referred=new_user).exists(), (
        f"Реферальная связь не создана. Существующие связи: {list(UserReferral.objects.all())}"
    )

@pytest.mark.django_db
def test_direct_registration_without_referral(client, valid_registration_data):
    """Тест обычной регистрации без реферальной ссылки"""
    response = client.post(reverse('auth:register'), data=valid_registration_data)

    assert response.status_code == 302
    assert User.objects.filter(username=valid_registration_data['username']).exists()

    # Проверяем, что реферальная связь не создана
    new_user = User.objects.get(username=valid_registration_data['username'])
    assert not UserReferral.objects.filter(referred=new_user).exists()

@pytest.mark.django_db
def test_multiple_referral_links(client, referral_user):
    """Тест создания нескольких реферальных ссылок для одного пользователя"""
    client.force_login(referral_user)

    # Первая ссылка
    response1 = client.get(reverse('referral:create', kwargs={'pk': referral_user.id}))
    data1 = response1.json()
    assert data1['status'] == 'created'

    # Вторая ссылка - должна вернуть существующую
    response2 = client.get(reverse('referral:create', kwargs={'pk': referral_user.id}))
    data2 = response2.json()
    assert data2['status'] == 'exists'
    assert data1['token'] == data2['token']

    # Проверяем, что создана только одна ссылка
    assert ReferralLink.objects.filter(user=referral_user).count() == 1

@pytest.mark.django_db
def test_referral_link_renewal(client, referral_user, referral_link):
    """Тест обновления просроченной ссылки"""
    client.force_login(referral_user)

    # Делаем ссылку просроченной
    referral_link.expires_at = timezone.now() - timedelta(days=1)
    referral_link.save()

    # Запрашиваем новую ссылку
    response = client.get(reverse('referral:create', kwargs={'pk': referral_user.id}))
    data = response.json()

    assert data['status'] == 'created'
    updated_link = ReferralLink.objects.get(pk=referral_link.pk)
    assert updated_link.token != referral_link.token
    assert updated_link.expires_at > timezone.now()

@pytest.mark.django_db
def test_referral_link_unique_token(referral_user):
    """Тест уникальности токена реферальной ссылки"""
    link1 = ReferralLink.objects.create(user=referral_user)
    link2 = ReferralLink.objects.create(user=referral_user)

    assert link1.token != link2.token

@pytest.mark.django_db
def test_referral_status_after_registration(client, referral_user, referral_link, valid_registration_data):
    """Тест статуса реферала после регистрации"""
    client.get(reverse('referral:link', kwargs={'token': referral_link.token}))
    assert 'referral_token' in client.session
    assert client.session['referral_token'] == referral_link.token

    client.post(reverse('auth:register'), data=valid_registration_data)
    assert User.objects.filter(username=valid_registration_data['username']).exists()

    new_user = User.objects.get(username=valid_registration_data['username'])
    referral = UserReferral.objects.get(referrer=referral_user, referred=new_user)
    assert referral.status == ReferralChoices.COMPLETED
