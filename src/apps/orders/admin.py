from django.contrib import admin

from apps.orders.models import Order, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "is_complete", "created_at")
    list_filter = ("is_complete", "created_at")
    search_fields = ("id", "customer__email")
    list_display_links = ("id", "customer")
    list_editable = ("is_complete",)
    readonly_fields = ("id", "customer", "created_at")
    ordering = ("-created_at",)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    list_filter = ("order", "product")
    list_display_links = ("id", "order")
    list_editable = ("quantity", "price")
    readonly_fields = ("id", "order", "product")
    ordering = ("-id",)
