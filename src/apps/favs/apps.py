from django.apps import AppConfig


class FavsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.favs"

    def ready(self):
        from . import signals
