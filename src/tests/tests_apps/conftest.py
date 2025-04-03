import pytest
from django.contrib.auth import get_user_model


@pytest.fixture()
def user(transactional_db):
    User = get_user_model()
    user = User.objects.create_user(username="test_user")
    user.set_password("test_user")
    user.save()
    return user
