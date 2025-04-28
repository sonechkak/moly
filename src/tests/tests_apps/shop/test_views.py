import pytest
from django.urls import reverse

from apps.shop.models import (
    Category,
    Product,
    Review
)


@pytest.mark.django_db
def test_index_page(client, products, categories):
    """Тестирование главной страницы."""
    response = client.get(reverse("shop:index"))
    assert response.status_code == 200
    assert "products" in response.context
    assert "title" in response.context
    assert response.context["title"] == "Главная страница"
    assert response.context["products"].count() == 12


@pytest.mark.django_db
def test_all_products_page(client, products):
    """Тестирование страницы с продуктами."""
    response = client.get(reverse("shop:all_products"))

    assert response.status_code == 200
    assert "products" in response.context
    assert "title" in response.context
    assert response.context["title"] == "Все товары"
    assert response.context["products"].count() == 12


# @pytest.mark.django_db
# def test_product_detail_page(client, product):
#     """Тестирование страницы с деталями продукта."""
#     response = client.get(reverse("shop:product_detail", kwargs={"slug": product.slug}))
#
#     assert response.status_code == 200
#     assert "product" in response.context
#     assert "title" in response.context
#     assert response.context["title"] == product.title
#     assert response.context["product"].title == product.title
#     assert response.context["product"].price == product.price


@pytest.mark.django_db
def test_category_list_page(client, categories, products):
    """Тестирование страницы с продуктами по категориям."""
    response = client.get(reverse("shop:category_list", kwargs={"slug": categories[0].slug}))

    assert response.status_code == 200
    assert "products" in response.context
    assert "title" in response.context
    assert response.context["title"] == f"Товары по категории: {categories[0].title}"
    assert list(response.context["products"]) == list(Product.objects.filter(category=categories[0]))
    assert list(response.context["categories"]) == list(Category.objects.filter(parent=None))


@pytest.mark.django_db
def test_add_review_valid(client, product, user):
    """Тестирование страницы добавления отзыва."""
    client.force_login(user)
    url = reverse("shop:add_review", kwargs={"pk": product.pk})
    data = {
        "text": "Отличный продукт!",
        "grade": 5,
    }
    response = client.post(url, data)

    assert response.status_code == 302
    review = Review.objects.get(product=product, author=user)
    assert review.text == data["text"]
    assert review.grade == str(data["grade"])
