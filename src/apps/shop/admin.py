from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Product,
    Gallery,
    Review,
    Mail,
    Customer,
    Order,
    OrderProduct,
    ShippingAddress,
)


class GalleryInline(admin.TabularInline):
    """Gallery Inline."""
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin."""
    list_display = ('title', 'parent', 'image_tag', 'get_product_count')
    search_fields = ('title',)
    list_filter = ('parent',)
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_product_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        return "0"

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.image.url))

    get_product_count.short_description = 'Количество товаров'
    image_tag.short_description = 'Изображение категории'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product Admin."""
    list_display = ('pk', 'title', 'price', 'quantity', 'price', 'size', 'color', 'available', 'get_image')
    list_editable = ('price', 'quantity', 'size', 'color', 'available')
    search_fields = ('title',)
    list_filter = ('title', 'price', 'quantity', 'available')
    list_display_links = ('pk', 'title')
    ordering = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (GalleryInline,)
    readonly_fields = ('watched',)

    def get_image(self, obj):
        if obj.images.filter(is_main=True).exists():
            image = obj.images.filter(is_main=True).first().image.url
            return mark_safe('<img src="{}" width="75" />'.format(image))
        else:
            return "Изображение отсутствует"

    get_image.short_description = 'Изображение товара'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Gallery Admin."""
    list_display = ('product', 'image')
    list_filter = ('product',)
    ordering = ('product',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin."""
    list_display = ('author', 'created_at', 'text')
    readonly_fields = ('author', 'created_at', 'text')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    """Mail spam Admin."""
    list_display = ('email', 'user')
    readonly_fields = ('email', 'user')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer Admin."""
    list_display = ('user', 'first_name', 'last_name', 'email')
    readonly_fields = ('user', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin."""
    list_display = ('customer', 'created_at', 'is_completed', 'shipping', 'pickup')
    readonly_fields = ('customer', 'created_at', 'shipping', 'pickup')
    ordering = ('-created_at',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    """Order products Admin."""
    list_display = ('product', 'order', 'quantity', 'added_at')
    readonly_fields = ('product', 'order', 'quantity', 'added_at')
    ordering = ('-added_at',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """Shipping addresses Admin."""
    list_display = ('customer', 'order', 'city', 'created_at')
    readonly_fields = ('customer', 'order', 'city', 'state', 'street', 'created_at')
    ordering = ('-created_at',)
