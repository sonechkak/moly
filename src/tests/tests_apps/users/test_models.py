import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import (
    Profile,
    ShippingAddress
)


@pytest.mark.django_db
def test_create_user(transactional_db, user):
        assert user.username == 'test_user'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser(transactional_db, admin_user):
    assert admin_user.username == 'admin'
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True


@pytest.mark.django_db
def test_creation_profile(transactional_db, user):
    profile, created = Profile.objects.get_or_create(
        user=user,
    )
    assert profile.user.username == 'test_user'
    assert profile.user.is_active is True
    assert profile.user.is_staff is False
    assert profile.user.is_superuser is False


@pytest.mark.django_db
def test_avatar_upload(transactional_db, temp_media_root, profile):
    avatar = SimpleUploadedFile(
        name='test_avatar.jpg',
        content=b'simple image content',
        content_type='image/jpeg'
    )
    profile.avatar = avatar
    profile.save(update_fields=['avatar'])
    assert 'test_avatar' in profile.avatar.name


@pytest.mark.django_db
def test_str_method_with_names(transactional_db, profile):
    assert str(profile) == "Test User"

@pytest.mark.django_db
def test_str_method_without_names(transactional_db, profile_without_names):
    assert str(profile_without_names) == "Test User"


@pytest.mark.django_db
def test_address_creation(transactional_db, shipping_address, profile):
    assert shipping_address.customer == profile
    assert shipping_address.city == 'Moscow'
    assert shipping_address.street == 'Lenina'
    assert shipping_address.house == '10'
    assert shipping_address.apartment == '15'
    assert shipping_address.is_primary is True

@pytest.mark.django_db
def test_address_str_method(transactional_db, shipping_address):
    assert str(shipping_address) == 'Moscow, Lenina, 10, 15'


@pytest.mark.django_db
def test_address_verbose_names(transactional_db):
    assert ShippingAddress._meta.verbose_name == 'Адрес доставки'
    assert ShippingAddress._meta.verbose_name_plural == 'Адреса доставки'
