from django.contrib import admin

from .models import Cashback


@admin.register(Cashback)
class CashbackAdmin(admin.ModelAdmin):
    """Admin view for Cashback model."""

    list_display = ("user", "order", "amount", "cashback_status", "created_at")
    list_filter = ("cashback_status",)
    search_fields = ("user__username", "order__id")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
