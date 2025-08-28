import logging

from apps.coupons.models import Coupon
from conf.celery import celery_app
from django.template.loader import render_to_string

from .models import Subscribe
from .service import SubscribeService

logger = logging.getLogger(__name__)


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
        if subscriber.product.has_price_changed:
            mail = SubscribeService(subscribe=subscriber)
            mail.send_template_mail()

    # Общая рассылка
    is_general_subs = subscribers.filter(is_general=True)
    for subscriber in is_general_subs:
        mail = SubscribeService(subscribe=subscriber)
        mail.send_template_mail()


@celery_app.task
def send_referral_coupon_email(subscribe_id, coupon_id):
    """Отправка купона на email подписчика."""

    try:
        subscriber = Subscribe.objects.get(id=subscribe_id)
        coupon = Coupon.objects.get(id=coupon_id)

        subject = "Ваш купон"
        message = f"Ваш купон: {coupon.code} на скидку {coupon.discount}%"
        html_message = render_to_string("subscribers/coupon_email.html", {"coupon": coupon})
        SubscribeService.send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[subscriber.email],
        )
        logger.info(f"Реферальный купон отправлен на {subscriber.email}")

    except Coupon.DoesNotExist:
        logger.error("Ошибка отправки реферального купона.")
