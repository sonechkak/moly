from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from utils.db import TimeStamp


User = get_user_model()


class Category(TimeStamp, models.Model):
    """Класс категорий."""
    title = models.CharField(max_length=255, verbose_name="Наименование категории")
    image = models.ImageField(upload_to="categories/%Y/%m/%d/", null=True, blank=True, verbose_name="Изображение категории")
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="subcategories"
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        """Ссылка на страницу категории."""
        return reverse("shop:category_list", kwargs={"slug": self.slug})

    def get_parent_category_image(self):
        """Для получения картинки родительской категории."""
        if self.image:
            return self.image.url
        return "Нет изображения"

    def get_new_products(self, hours=1):
        """Возвращает товары, которые добавились в категории."""
        from django.utils import timezone
        from datetime import timedelta
        # Queryset товаров, которые добавлены за последний час
        return self.products.filter(created_at__gte=timezone.now() - timedelta(hours=hours))

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']


class Product(TimeStamp, models.Model):
    """Класс товаров."""
    title = models.CharField(max_length=255, verbose_name="Наименование товара")
    price = models.IntegerField(verbose_name="Цена товара")
    watched = models.IntegerField(default=0, verbose_name="Количество просмотров")
    quantity = models.IntegerField(default=0, verbose_name="Количество товара на складе")
    description = models.TextField(default="Скоро здесь будет описание товара...", verbose_name="Описание товара")
    info = models.TextField(default="Дополнительная информация о товаре", verbose_name="Информация о товаре")
    category = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
        verbose_name="Категория товара"
    )
    slug = models.SlugField(unique=True, null=True, verbose_name="Slug товара")
    size = models.IntegerField(default=30, verbose_name="Размер в мм")
    color = models.TextField(max_length=30, default="Стандартный", verbose_name="Цвет/Материал")
    brand = models.CharField(max_length=150, default="Apple", verbose_name="Бренд товара")
    available = models.BooleanField(default=True, verbose_name="Доступны к заказу")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Товар: pk={self.pk}, title={self.title}, price={self.price}, quantity={self.quantity}"

    def get_absolute_url(self):
        """Возвращает детальную страницу товара."""
        return reverse("shop:product_detail", kwargs={"slug": self.slug})

    def get_main_photo(self):
        """Возвращает основное фото."""
        if self.images.filter(is_main=True).exists():
            return self.images.get(is_main=True).image.url
        return mark_safe(f'<img src="/media/products/default.png" width="50" height="50">')

    def has_changed(self):
        """Возвращает bool, если товар был изменен."""
        from datetime import timedelta
        from django.utils import timezone
        return self.updated_at >= timezone.now() - timedelta(hours=1)

    def old_price(self):
        """Возвращает цену на 20% больше текущей."""
        return self.price * 1.2

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['available', '-created_at']


class Gallery(models.Model):
    """Класс для изображений товаров."""
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")

    def __str__(self):
        return self.product.title

    def __repr__(self):
        return f"Изображение: pk={self.pk}, product={self.product.title}, is_main={self.is_main}"

    def save(self, *args, **kwargs):
        if self.is_main:
            self.product.images.update(is_main=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Review(TimeStamp, models.Model):
    """Модель для отзывов."""

    CHOICES = (
        ('5', 'Отлично'),
        ('4', 'Хорошо'),
        ('3', 'Средне'),
        ('2', 'Плохо'),
        ('1', 'Очень плохо'),
    )

    grade = models.CharField(max_length=20, choices=CHOICES, blank=True, null=True, verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Продукт")
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
