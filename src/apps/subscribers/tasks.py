from conf.celery import celery_app

from .models import Subscribe
from .service import SubscribeService


@celery_app.task
def send_subscriber_email():
    """Функция для отправки писем подписчикам."""
    subscribers = Subscribe.objects.filter(user__is_active=True, user__email__isnull=False)

    # Для категорий
    category_subs = subscribers.filter(category__isnull=False)
    for subscriber in category_subs:
        new_products = subscriber.category.get_new_products(hours=24)
        if new_products:
            mail = SubscribeService(subscribe=subscriber)
            mail.send_template_mail()

    # Для товаров
    product_subs = subscribers.filter(product__isnull=False)
    for subscriber in product_subs:
        if subscriber.product.has_changed:
            mail = SubscribeService(subscribe=subscriber)
            mail.send_template_mail()

    # Общая рассылка
    is_general_subs = subscribers.filter(is_general=True)
    for subscriber in is_general_subs:
        mail = SubscribeService(subscribe=subscriber)
        mail.send_template_mail()
