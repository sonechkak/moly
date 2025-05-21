from apps.notifications.models import Notification


def get_unread_count(user):
    """Получить количество непрочитанных уведомлений"""
    return Notification.objects.filter(user=user, status="pending").count()
