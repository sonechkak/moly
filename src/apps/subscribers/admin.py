from django.contrib import admin

from .models import Subscribe


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Админка подписок."""
    list_display = ("email", "user", "product", "category", "is_general")
    list_filter = ("is_general",)
    search_fields = ("email",)
    list_per_page = 10
    list_display_links = ("email",)
