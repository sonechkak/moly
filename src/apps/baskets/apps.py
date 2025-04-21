from django.apps import AppConfig


class BasketConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.baskets"

    def ready(self):
        import apps.baskets.signals
