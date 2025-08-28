import logging

from apps.coupons.models import Coupon
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Subscribe

logger = logging.getLogger("user.actions")


class SubscribeService:
    """Класс для отправки писем подписчикам."""

    def __init__(self, subscribe: Subscribe):
        self.subscribe = subscribe

    def send_coupon_email(self, coupon: Coupon):
        """Отправка купона на email подписчика."""

        subject = "Ваш купон"
        message = f"Ваш купон: {coupon.code} на скидку {coupon.discount}%"
        html_message = render_to_string("subscribers/coupon_email.html", {"coupon": coupon})
        self.send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[self.subscribe.email],
        )

    def send_template_mail(self):
        """Отправка письма с шаблоном."""
        subject = "Moly: Новые поступления Apple со скидкой!"
        message = (
            "В нашем магазине появились новые товары Apple со скидками до 15%: iPhone 15 Pro, MacBook Air и другие."
        )
        html_message = render_to_string("subscribers/template_mail.html", {"title": subject})
        self.send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[self.subscribe.email],
        )

    def send_notification_mail(self):
        """Отправка уведомлений подписчикам."""
        subject = "Уведомление о новом товаре."
        message = "Уведомление о новом товаре."
        self.send_mail(
            subject=subject,
            message=message,
            recipient_list=[self.subscribe.email],
        )

    @staticmethod
    def send_mail(subject, message, recipient_list, html_message=None):
        """Отправка письма."""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                html_message=html_message,
            )
            logger.info("Письмо доставлено.")
        except Exception as e:
            logger.error("Письмо не доставлено. Ошибка: %s", e)
