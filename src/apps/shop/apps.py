from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.shop"
    app_label = "shop"

    def ready(self):
        from . import signals
