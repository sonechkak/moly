from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import (
    Profile,
    ShippingAddress
)
from tests.tests_apps.conftest import avatar


class TestUserModel:
    def test_create_user(self, user):
        assert user.username == 'test_user'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self, admin_user):
        assert admin_user.username == 'admin'
        assert admin_user.is_active is True
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True


class TestProfileModel:
    def test_creation_profile(self, user):
        profile, created = Profile.objects.get_or_create(
            user=user,
        )
        assert profile.user.username == 'test_user'
        assert profile.user.is_active is True
        assert profile.user.is_staff is False
        assert profile.user.is_superuser is False

    def test_avatar_upload(self, temp_media_root, profile):
        avatar = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'simple image content',
            content_type='image/jpeg'
        )
        profile.avatar = avatar
        profile.save(update_fields=['avatar'])
        assert 'test_avatar' in profile.avatar.name

    def test_str_method_with_names(self, profile):
        assert str(profile) == "Test User"

    def test_str_method_without_names(self, profile_without_names):
        assert str(profile_without_names) == "Test User"


class TestShippingAddressModel:
    def test_address_creation(self, shipping_address, profile):
        assert shipping_address.customer == profile
        assert shipping_address.city == 'Moscow'
        assert shipping_address.street == 'Lenina'
        assert shipping_address.house == '10'
        assert shipping_address.apartment == '15'
        assert shipping_address.is_primary is True

    def test_address_str_method(self, shipping_address):
        assert str(shipping_address) == 'Moscow, Lenina, 10, 15'

    def test_address_verbose_names(self):
        assert ShippingAddress._meta.verbose_name == 'Адрес доставки'
        assert ShippingAddress._meta.verbose_name_plural == 'Адреса доставки'
