from apps.shop.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView, ListView

from .models import Notification, ProductAvalaibilityNotification
from .services.get_unread_count import get_unread_count


class AllNotificationsView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/all_notifications.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)

        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        notification_type = self.request.GET.get("type")
        if notification_type:
            queryset = queryset.filter(type=notification_type)

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update(
            {
                "title": "Все уведомления",
                "unread_notifications_count": get_unread_count(user=user),
                "notifications": Notification.objects.filter(user=user)[:6],
            }
        )
        return context


class DeleteNotificationView(LoginRequiredMixin, View):
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.delete()
        messages.success(request, "Уведомление успешно удалено.")

        next_url = request.POST.get("next", reverse("notifications:all"))
        return redirect(next_url)


class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)

        if notification.status != "read":
            notification.status = "read"
            notification.read_at = timezone.now()
            notification.save()
            messages.success(request, "Уведомление отмечено как прочитанное.")

        next_url = request.POST.get("next", reverse("notifications:all"))
        return redirect(next_url)


class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request):
        unread_notifications = Notification.objects.filter(user=request.user, status="pending")

        count = unread_notifications.count()

        if count > 0:
            unread_notifications.update(status="read", read_at=timezone.now())
            messages.success(request, f"{count} уведомлений отмечено как прочитанные.")

        next_page = self.request.META.get("HTTP_REFERER", reverse("notifications:all"))
        return redirect(next_page)


class SubscribeToProductView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        subscription, created = ProductAvalaibilityNotification.objects.get_or_create(
            user=request.user,
            product=product,
        )

        if created:
            messages.success(request, f'Вы успешно подписались на уведомления о доступности товара "{product.title}".')
        else:
            messages.info(request, f'Вы уже подписаны на уведомления о доступности товара "{product.title}".')

        next_page = self.request.META.get("HTTP_REFERER", reverse("shop:product_detail", kwargs={"slug": product.slug}))
        return redirect(next_page)


class UnsubscribeFromProductView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        try:
            subscription = ProductAvalaibilityNotification.objects.get(user=request.user, product=product)
            subscription.delete()
            messages.success(request, f'Вы отписались от уведомлений о доступности товара "{product.title}".')
        except ProductAvalaibilityNotification.DoesNotExist:
            messages.info(request, "Вы не были подписаны на уведомления о доступности этого товара.")

        next_page = self.request.META.get("HTTP_REFERER", reverse("shop:product_detail", kwargs={"slug": product.slug}))
        return redirect(next_page)


class SubscribedProductsView(LoginRequiredMixin, ListView):
    model = ProductAvalaibilityNotification
    template_name = "notifications/subscribed_products.html"
    context_object_name = "subscriptions"
    paginate_by = 10

    def get_queryset(self):
        return ProductAvalaibilityNotification.objects.filter(user=self.request.user).select_related("product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мои подписки на товары"
        return context
