from django.db import models


class TimeStamp(models.Model):
    """Класс для установления дат."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
