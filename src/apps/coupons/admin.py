from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Админ панель для купонов."""

    list_display = ("code", "discount", "valid_from", "valid_to", "is_active")
    search_fields = ("code",)
    list_filter = ("is_active", "valid_from", "valid_to")
    ordering = ("-valid_from", "-valid_to")
    date_hierarchy = "valid_from"
    list_editable = ("is_active",)
