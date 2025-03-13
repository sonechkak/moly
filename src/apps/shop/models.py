from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class Category(models.Model):
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

    def get_parent_category_image(self):
        """Для получения картинки родительской категории."""
        if self.image:
            return self.image.url
        return "Нет изображения"

    def get_absolute_url(self):
        """Ссылка на страницу категории."""
        return reverse("shop:category_list", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Категория: pk={self.pk}, title={self.title}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']


class Product(models.Model):
    """Класс товаров."""
    title = models.CharField(max_length=255, verbose_name="Наименование товара")
    price = models.FloatField(verbose_name="Цена товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
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

    def get_main_photo(self):
        if self.images.filter(is_main=True).exists():
            return self.images.get(is_main=True).image.url
        return mark_safe(f'<img src="/media/products/default.jpg" width="50" height="50">')

    def get_absolute_url(self):
        pass

    def old_price(self):
        """Возвращает цену на 20% больше текущей."""
        return self.price * 1.2

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Товар: pk={self.pk}, title={self.title}, price={self.price}, quantity={self.quantity}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['available', '-created_at']


class Gallery(models.Model):
    """Класс для изображений товаров."""
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")

    def save(self, *args, **kwargs):
        if self.is_main:
            self.product.images.update(is_main=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.product.title

    def __repr__(self):
        return f"Изображение: pk={self.pk}, product={self.product.title}, is_main={self.is_main}"
