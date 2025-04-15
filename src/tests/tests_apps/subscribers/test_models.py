import pytest
from django.core.exceptions import ValidationError

from apps.subscribers.models import Subscribe


@pytest.mark.django_db
def test_create_subscribe_with_email_only():
    """Тест создания подписки только с email."""
    subscribe = Subscribe.objects.create(email="test@mail.ru")
    assert subscribe.email == subscribe.email
    assert subscribe.user is None
    assert subscribe.product is None
    assert subscribe.category is None
    assert subscribe.is_general is True


@pytest.mark.django_db
def test_create_subscribe_with_user_only(user):
    """Тест создания подписки только с пользователем."""
    subscribe = Subscribe.objects.create(user=user)
    assert subscribe.user == user
    assert subscribe.email is None
    assert subscribe.product is None
    assert subscribe.category is None
    assert subscribe.is_general is True


@pytest.mark.django_db
def test_create_subscribe_with_product(user, product):
    """Тест создания подписки с продуктом."""
    subscribe = Subscribe.objects.create(user=user, product=product)
    assert subscribe.user == user
    assert subscribe.product == product
    assert subscribe.is_general is False


@pytest.mark.django_db
def test_create_subscribe_with_category(user, category):
    """Тест создания подписки с категорией."""
    subscribe = Subscribe.objects.create(user=user, category=category)
    assert subscribe.user == user
    assert subscribe.category == category
    assert subscribe.is_general is False


@pytest.mark.django_db
def test_is_general_set_to_false_with_product_or_category(product, category):
    """Тест, что is_general устанавливается в False при наличии product или category."""
    # С продуктом
    subscribe1 = Subscribe(email="test1@example.com", product=product)
    subscribe1.save()
    assert subscribe1.is_general is False

    # С категорией
    subscribe2 = Subscribe(email="test2@example.com", category=category)
    subscribe2.save()
    assert subscribe2.is_general is False

    # С продуктом и категорией
    subscribe3 = Subscribe(email="test3@example.com", product=product, category=category)
    subscribe3.save()
    assert subscribe3.is_general is False


@pytest.mark.django_db
def test_str_representation():
    """Тест строкового представления."""
    subscribe = Subscribe.objects.create(email="test@example.com")
    assert str(subscribe) == "test@example.com"


@pytest.mark.django_db
def test_str_representation_with_user(user):
    """Тест строкового представления с пользователем."""
    subscribe = Subscribe.objects.create(user=user)

    assert str(subscribe) == user.email


@pytest.mark.django_db
def test_invalid_email():
    """Тест невалидного email."""
    with pytest.raises(ValidationError):
        subscribe = Subscribe(email="invalid_email")
        subscribe.full_clean()
        subscribe.save()


@pytest.mark.django_db
def test_blank_and_null_fields():
    """Тест, что все поля могут быть blank и null."""
    subscribe = Subscribe.objects.create()
    assert subscribe.email is None
    assert subscribe.user is None
