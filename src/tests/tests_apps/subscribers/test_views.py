import pytest
from django.urls import reverse

from apps.subscribers.models import Subscribe


@pytest.fixture
def test_save_subscribe(client):
    email = "testemail@test.com"
    url = reverse("subscribers:subscribe")
    client.post(url, data={"email": email})

    assert Subscribe.objects.get(email=email).email == email
    assert Subscribe.objects.count() == 1
