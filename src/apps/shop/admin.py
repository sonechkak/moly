from django.contrib import admin

from .models import (
    Brand,
    Category,
    Gallery,
    Product,
    Review,
)


class GalleryInline(admin.TabularInline):
    """Gallery Inline."""

    fk_name = "product"
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin."""

    list_display = ("title", "parent", "image_tag", "get_product_count")
    search_fields = ("title",)
    list_filter = ("parent",)
    ordering = ("title",)
    prepopulated_fields = {"slug": ("title",)}

    def get_product_count(self, obj):
        """Возвращает количество товаров в категории."""
        if obj.products:
            return str(len(obj.products.all()))
        return "0"

    def image_tag(self, obj):
        """Возвращает изображение категории."""
        return obj.image.url if obj.image else None

    get_product_count.short_description = "Количество товаров"
    image_tag.short_description = "Изображение категории"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Админка для брендов."""

    list_display = ("id", "title", "image", "slug")
    list_filter = ("title",)
    search_fields = ("title",)
    ordering = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("id",)

    def get_image_tag(self, obj):
        """Возвращает изображение бренда."""
        return obj.image.url if obj.image else None


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product Admin."""

    list_display = ("pk", "title", "price", "quantity", "size", "color", "available", "get_image")
    list_editable = ("price", "quantity", "size", "color", "available")
    search_fields = ("title",)
    list_filter = ("title", "price", "quantity", "available")
    list_display_links = ("pk", "title")
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = (GalleryInline,)
    readonly_fields = ("watched",)

    def get_image(self, obj):
        """Возвращает изображение товара."""
        return obj.image.url if obj.get_main_photo else None

    get_image.short_description = "Изображение товара"


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Gallery Admin."""

    list_display = ("product", "image")
    list_filter = ("product",)
    ordering = ("product",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin."""

    list_display = ("author", "created_at", "text")
    readonly_fields = ("author", "created_at", "text")
