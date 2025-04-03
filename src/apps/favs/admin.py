from apps.favs.models import FavoriteProducts
from django.contrib import admin


@admin.register(FavoriteProducts)
class FavoriteProductseAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    readonly_fields = ("user", "product")
    search_fields = ("user", "product")
    list_filter = ("user", "product")
    ordering = ("user",)
