from django.contrib import admin

from .models import LoyaltyLevel, Privilege, UserLoyalty


@admin.register(LoyaltyLevel)
class LoyaltyLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "min_points", "cashback_percentage", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("order",)


@admin.register(UserLoyalty)
class UserLoyaltyAdmin(admin.ModelAdmin):
    list_display = ("user", "current_level", "total_spent", "cashback", "updated_at")
    list_filter = ("current_level",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("cashback", "total_spent", "updated_at")

    fieldsets = (
        (None, {"fields": ("user", "current_level")}),
        ("Финансовая информация", {"fields": ("total_spent", "cashback", "updated_at")}),
    )


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    list_filter = ("loyalty_level",)
    ordering = ("loyalty_level", "name")
