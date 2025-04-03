from django.contrib import admin

from .models import Profile, ShippingAddress


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админка профиля пользователя."""

    list_display = ("user", "first_name", "last_name", "email", "phone")
    list_filter = ("user", "first_name", "last_name", "email", "phone")
    search_fields = ("first_name", "last_name", "email", "phone")
    empty_value_display = "-пусто-"


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """Админка адреса доставки."""

    list_display = ("customer", "city", "state", "street", "house", "apartment", "zipcode")
    list_filter = ("customer", "city", "state", "street", "house", "apartment", "zipcode")
    search_fields = ("city", "state", "street", "house", "apartment", "zipcode")
    empty_value_display = "-пусто-"
