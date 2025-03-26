from apps.subscribers.models import Subscribe
from conf.celery import celery_app


@celery_app.task
def send_subscriber_email():
    """Функция для отправки писем подписчикам."""
    subscribers = Subscribe.objects.filter(user__is_active=True, user__email__isnull=False)
    category = subscribers.filter(category__isnull=False)
    product = subscribers.filter(product__isnull=False)
    is_general = subscribers.filter(is_general=True)
