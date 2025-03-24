from django.contrib import admin

from .models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """Админка для корзины."""
    list_display = ("user",)
    list_filter = ("user",)
    ordering = ("user",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 10
    date_hierarchy = "created_at"
