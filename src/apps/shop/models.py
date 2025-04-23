from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from utils.db import TimeStamp

from .utils import get_brand_upload_path, get_category_upload_path, get_image_upload_path

User = get_user_model()


class Category(TimeStamp, models.Model):
    """Класс категорий."""

    title = models.CharField("Наименование категории", max_length=255)
    image = models.ImageField("Изображение категории", upload_to=get_category_upload_path)
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категория", related_name="subcategories"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Ссылка на страницу категории."""
        return reverse("shop:category_list", kwargs={"slug": self.slug})

    def get_parent_category_image(self):
        """Для получения картинки родительской категории."""
        return self.image.url if self.image else None

    def get_new_products(self, hours=1):
        """Возвращает товары, которые добавились в категории."""
        # Queryset товаров, которые добавлены за последний час
        return self.products.filter(created_at__gte=timezone.now() - timedelta(hours=hours))


class Brand(models.Model):
    """Класс для брендов."""

    title = models.CharField("Наименование бренда", max_length=255)
    image = models.ImageField("Изображение бренда", upload_to=get_brand_upload_path)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def __repr__(self):
        return {self.title}


class Product(TimeStamp, models.Model):
    """Класс товаров."""

    title = models.CharField("Наименование товара", max_length=255)
    price = models.PositiveIntegerField("Цена товара")
    previous_price = models.IntegerField("Предыдущая цена", null=True, blank=True, editable=False)
    watched = models.PositiveIntegerField("Количество просмотров", default=1)
    quantity = models.IntegerField("Количество товара на складе")
    description = models.TextField("Описание товара")
    info = models.TextField("Информация о товаре")
    category = models.ManyToManyField(Category, related_name="products", blank=True, verbose_name="Категория товара")
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField("Размер в мм", default=30)
    color = models.TextField("Цвет/Материал")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Бренд")
    available = models.BooleanField("Доступны к заказу", default=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["available", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Сохраняем предыдущую цену, если она изменилась
        if self.pk and self.price != self._original_price:
            self.previous_price = self._original_price

        super().save(*args, **kwargs)
        # Обновляем оригинальную цену
        self._original_price = self.price

    def get_absolute_url(self):
        """Возвращает детальную страницу товара."""
        return reverse("shop:product_detail", kwargs={"slug": self.slug})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_price = self.price

    def get_main_photo(self):
        """Возвращает основное фото."""
        if self.images.filter(is_main=True).exists():
            return self.images.get(is_main=True).image.url
        else:
            return self.images.first().image.url if self.images.exists() else None

    def old_price(self):
        """Возвращает цену на 20% больше текущей."""
        return self.price * 1.2

    @property
    def has_price_changed(self):
        """Возвращает True, если цена изменилась после последнего сохранения."""
        return self.price != self._original_price


class Gallery(models.Model):
    """Класс для изображений товаров."""

    image = models.ImageField("Изображение", upload_to=get_image_upload_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    is_main = models.BooleanField("Основное изображение", default=False)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if self.image:
            temp = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = temp
            kwargs.pop("force_insert", None)

        if self.is_main and self.product:
            self.product.images.update(is_main=False)
        super().save(*args, **kwargs)


class Review(TimeStamp, models.Model):
    """Модель для отзывов."""

    CHOICES = (
        ("5", "Отлично"),
        ("4", "Хорошо"),
        ("3", "Средне"),
        ("2", "Плохо"),
        ("1", "Очень плохо"),
    )

    grade = models.CharField("Оценка", max_length=20, choices=CHOICES, blank=True, null=True)
    text = models.TextField("Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Продукт")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text
