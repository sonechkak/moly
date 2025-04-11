import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from apps.users.models import *


User = get_user_model()


@pytest.fixture
def admin_user(transactional_db):
    return User.objects.create_superuser(username='admin', password='adminpass123')


@pytest.fixture
def profile(transactional_db, user):
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '+1234567890'
        }
    )
    return profile


@pytest.fixture
def profile_without_names(transactional_db, user):
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={}
    )
    return profile


@pytest.fixture
def shipping_address(transactional_db, profile):
    return ShippingAddress.objects.create(
        customer=profile,
        title='Home',
        city='Moscow',
        state='Moscow Oblast',
        street='Lenina',
        house='10',
        apartment='15',
        is_primary=True,
        recipient='John Doe',
        contact='+1234567890',
        zipcode='123456'
    )
