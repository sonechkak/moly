import pytest
from django.contrib.messages import get_messages
from django.urls import reverse


@pytest.mark.django_db
def test_cashback_apply_success(client, user):
    """Тест успешного применения кэшбэка."""
    client.force_login(user)
    apply_url = reverse('cashback:apply')

    # Добавляем cashback_amount в данные POST
    response = client.post(apply_url, {
        'use_cashback': True,
        'cashback_amount': 100  # Тестовая сумма
    }, follow=True)

    # Проверяем редирект
    assert response.redirect_chain[-1][0] == reverse('baskets:basket', kwargs={'pk': user.pk})

    messages = list(get_messages(response.wsgi_request))
    assert 'Кэшбэк успешно применен к заказу' in str(messages[0])
    assert client.session.get('use_cashback') is True
    assert client.session.get('cashback_amount') == 100
