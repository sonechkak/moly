import re
import pytest

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.shop.models import (
    Category,
    Gallery,
    Review,
)


@pytest.mark.django_db
def test_category_creation(category):
        assert category.title == "test_category"
        assert category.slug == "test_category"
        assert str(category) == "test_category"
        assert category.get_absolute_url() == reverse("shop:category_list", kwargs={"slug": "test_category"})


@pytest.mark.django_db
def test_parent_category(category):
    """Тест родительской категории"""
    child = Category.objects.create(
        title="child_category",
        slug="child_category",
        parent=category
    )
    assert child.parent == category
    assert child in category.subcategories.all()


@pytest.mark.django_db
def test_brand_creation(brand):
    """Тест создания бренда"""
    assert brand.title == "Apple"
    assert brand.slug == "apple"
    assert str(brand) == "Apple"


@pytest.mark.django_db
def test_product_creation(product, category, brand):
    """Тест создания продукта"""
    assert product.title == "Тестовый товар"
    assert product.price == 100
    assert category in product.category.all()
    assert product.brand == brand
    assert str(product) == "Тестовый товар"


@pytest.mark.django_db
def test_price_changes(product):
    """Тест отслеживания изменения цены"""
    original_price = product.price
    product.price = 150
    product.save()
    product.refresh_from_db()
    assert product.price == 150


@pytest.mark.django_db
def test_invalid_price_changes(product):
    """Тест отслеживания изменения цены"""
    original_price = product.price
    product.price = -150

    product.refresh_from_db()
    assert product.price == original_price


@pytest.mark.django_db
def test_get_main_photo(temp_media_root, product):
    """Тест получения главного фото"""
    from django.core.files.uploadedfile import SimpleUploadedFile
    image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    # Создаем галерею с главным изображением
    Gallery.objects.create(product=product, image=image, is_main=True)

    assert product.get_main_photo() is not None


@pytest.mark.django_db
def test_old_price_calculation(product):
    """Тест расчета старой цены"""
    assert product.old_price() == product.price * 1.2


@pytest.mark.django_db
def test_absolute_url(product):
    """Тест абсолютного URL продукта"""
    expected_url = reverse("shop:product_detail", kwargs={"slug": product.slug})
    assert product.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_gallery_creation(temp_media_root, product):
    """Тест создания галереи"""
    from django.core.files.uploadedfile import SimpleUploadedFile
    image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    gallery = Gallery.objects.create(product=product, image=image)
    assert str(gallery) == product.title
    assert gallery in product.images.all()


@pytest.mark.django_db
def test_main_image_logic(temp_media_root, product):
    """Тест логики главного изображения"""
    image1 = SimpleUploadedFile("test1.jpg", b"file_content", content_type="image/jpeg")
    image2 = SimpleUploadedFile("test2.jpg", b"file_content", content_type="image/jpeg")

    # Создаем первое изображение как главное
    gallery1 = Gallery.objects.create(product=product, image=image1, is_main=True)

    # Первое изображение стало главным
    assert Gallery.objects.filter(product=product, is_main=True).count() == 1
    assert Gallery.objects.get(product=product, is_main=True).id == gallery1.id

    # Создаем второе изображение как главное
    gallery2 = Gallery.objects.create(product=product, image=image2, is_main=True)

    # Проверяем что только второе изображение главное
    assert Gallery.objects.filter(product=product, is_main=True).count() == 1
    assert Gallery.objects.get(product=product, is_main=True).id == gallery2.id

    # Получаем текущее главное изображение
    main_image = Gallery.objects.get(product=product, is_main=True)

    # Проверяем путь загрузки изображения
    expected_path_pattern = re.compile(
        r'^upload/products/' + str(product.id) + r'/' + str(gallery2.id) + r'_.+\.jpg$'
    )
    assert expected_path_pattern.match(main_image.image.name) is not None


@pytest.mark.django_db
def test_review_creation(user, product):
    """Тест создания отзыва"""
    review = Review.objects.create(
        grade="5",
        text="Отличный товар!",
        author=user,
        product=product
    )

    assert str(review) == user.username
    assert review in product.reviews.all()
    assert review.grade == "5"
    assert review.text == "Отличный товар!"


@pytest.mark.django_db
def test_grade_choices_validation(user, product):
    """Тест валидации оценки"""
    with pytest.raises(ValidationError):
        Review.objects.create(
            grade="6",
            text="Тест",
            author=user,
            product=product
        ).full_clean()
