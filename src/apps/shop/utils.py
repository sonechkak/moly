import os
from django.utils.text import slugify
from random import randint


def get_category_upload_path(instance, filename):
    """Для загрузки изображений в папку categories."""
    try:
        name, ext = os.path.splitext(filename)  # Разделяем имя файла и расширение
        safe_name = f"{slugify(name)}.{ext.lower()}"  # Приводим имя к безопасному виду
    except ValueError:
        safe_name = filename  # используем оригинальное имя
    return f"upload/categories/{instance.id}/{safe_name}"


def get_image_upload_path(instance, filename):
    """Для загрузки изображений в папку products."""
    try:
        name, ext = os.path.splitext(filename)
        safe_name = f"{slugify(name)}.{ext.lower()}"
    except ValueError:
        safe_name = filename
    return f"upload/products/{instance.id}/{safe_name}"


def get_brand_upload_path(instance, filename):
    """Для загрузки изображений в папку brands."""
    try:
        # Разделяем имя файла и расширение
        name, ext = os.path.splitext(filename)
        # Приводим имя к безопасному виду
        safe_name = f"{slugify(name)}.{ext.lower()}"
    except ValueError:
        safe_name = filename
    return f"upload/brands/{instance.pk}/{safe_name}"


def get_random_products(product, products):
    """Получение случайных товаров для страницы товара."""
    data = []
    for i in range(6):
        random_index = randint(0, len(products) - 1)
        random_item = products[random_index]
        if random_item not in data and str(random_item) != product.title:
            data.append(random_item)

    return data
