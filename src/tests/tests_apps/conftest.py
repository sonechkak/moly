import pytest
from django.contrib.auth import get_user_model


@pytest.fixture()
def user(transactional_db):
    user = get_user_model()
    user = user.objects.create(username="test_user")
    user.set_password("test_user")
    user.save()
    return user
