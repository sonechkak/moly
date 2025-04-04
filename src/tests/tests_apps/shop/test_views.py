import pytest


@pytest.mark.django_db
def test_(client):
    """Тестирование главной страницы."""
    response = client.get("/")

    assert response.status_code == 200
    assert "products" in response.context
    assert "title" in response.context
    assert response.context["title"] == "Главная страница"
