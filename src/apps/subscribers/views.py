from apps.subscribers.models import Subscribe
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views import View


class SaveSubscribers(View):
    """Собирает почтовые адреса."""

    def post(self, request):
        email = request.POST.get("email")
        if email:
            subscribers = Subscribe.objects.all()
            if subscribers.filter(email=email).exists():
                messages.error(request, "Вы уже подписаны на наши новости.")
            else:
                try:
                    subscriber = Subscribe(email=email)
                    subscriber.save()
                    messages.success(request, "Вы успешно подписались на наши новости.")
                except Exception:
                    messages.error(request, "Произошла ошибка.")

        return redirect("shop:index")
