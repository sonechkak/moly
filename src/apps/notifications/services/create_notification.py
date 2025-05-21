from apps.notifications.models import Notification


def create_notification(user, title, message, notification_type, url=None):
    """Создание уведомления."""
    notification = Notification.objects.create(
        user=user, title=title, message=message, type=notification_type, status="pending", url=url
    )
    return notification
