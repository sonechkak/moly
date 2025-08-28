from apps.notifications.models import Notification
from django.utils import timezone


def mark_as_read(pk, user):
    """Отметить уведомление как прочитанное."""

    notification = Notification.objects.get(pk=pk, user=user)
    notification.status = "READ"
    notification.read_at = timezone.now()
    notification.save(update_fields=["status", "read_at"])
