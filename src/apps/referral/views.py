from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .models import ReferralLink, generate_token


class ReferralLinkView(View):
    """Обработка перехода по реферальной ссылке."""

    def get(self, request, token, *args, **kwargs):
        # Получаем ссылку или 404
        link = get_object_or_404(ReferralLink, token=token, is_active=True, expires_at__gte=timezone.now())

        request.session["referral_token"] = token
        request.session.set_expiry(86400)  # 24 часа

        ReferralLink.objects.filter(pk=link.pk).update(clicks=models.F("clicks") + 1)

        return redirect("auth:register")


class ReferralLinkCreate(LoginRequiredMixin, View):
    """Создание реферальной ссылки."""

    login_url = "auth:login"

    def get(self, request, *args, **kwargs):
        referral_link, created = ReferralLink.objects.get_or_create(
            user=request.user, defaults={"expires_at": timezone.now() + timedelta(days=30)}
        )

        if not created and referral_link.expires_at < timezone.now():
            referral_link.token = generate_token()
            referral_link.expires_at = timezone.now() + timedelta(days=30)
            referral_link.save()
            created = True

        return JsonResponse(
            {
                "status": "created" if created else "exists",
                "token": referral_link.token,
                "referral_url": request.build_absolute_uri(
                    reverse("referral:link", kwargs={"token": referral_link.token})
                ),
                "expires_at": referral_link.expires_at.isoformat(),
                "clicks": referral_link.clicks,
            }
        )
