import logging

from apps.subscribers.models import Subscribe
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render


def save_subscribers(request):
    """Собирает почтовые адреса."""
    email = request.POST.get("email")
    user = request.user if request.user.is_authenticated else None
    if email:
        try:
            Subscribe.objects.create(email=email, user=user)
        except IntegrityError:
            messages.error(request, "Вы уже подписались на новости.")

    return redirect("shop:index")


def send_mail_to_customers(request):
    """Отправка сообщений подписчикам."""
    from django.core.mail import send_mail

    if request.method == "POST":
        text = request.POST.get("text")
        mail_list = Subscribe.objects.all()
        for email in mail_list:
            send_mail(
                subject="У вас новая акция",
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email.email],
                fail_silently=False,
            )
            send_mail = True
            logging.INFO(f"Письмо отправлено на {email.email}")

    context = {"title": "Спамер"}
    return render(request, "shop/send_mail.html", context)
