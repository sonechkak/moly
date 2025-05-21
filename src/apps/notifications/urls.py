from django.urls import path

from .views import (
    AllNotificationsView,
    DeleteNotificationView,
    MarkAllNotificationsReadView,
    MarkNotificationReadView,
    SubscribedProductsView,
    SubscribeToProductView,
    UnsubscribeFromProductView,
)

app_name = "notifications"


urlpatterns = [
    path("notifications/all/", AllNotificationsView.as_view(), name="all"),
    path("notifications/<int:notification_id>/mark_read/", MarkNotificationReadView.as_view(), name="mark_read"),
    path("notifications/mark_all_read/", MarkAllNotificationsReadView.as_view(), name="mark_all_read"),
    path("notifications/<int:notification_id>/delete/", DeleteNotificationView.as_view(), name="delete"),
    path("product/<int:product_id>/subscribe/", SubscribeToProductView.as_view(), name="product_subscribe"),
    path("product/<int:product_id>/unsubscribe/", UnsubscribeFromProductView.as_view(), name="product_unsubscribe"),
    path("product/all/subscrubed/", SubscribedProductsView.as_view(), name="subscribed_products"),
]
