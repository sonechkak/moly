from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("apps.shop.urls"), name="shop"),
    path("", include("apps.authentications.urls"), name="auth"),
    path("", include("apps.baskets.urls"), name="baskets"),
    path("", include("apps.favs.urls"), name="favs"),
    path("", include("apps.orders.urls"), name="orders"),
    path("", include("apps.subscribers.urls"), name="subscribers"),
    path("", include("apps.users.urls"), name="users"),
    path("", include("apps.coupons.urls"), name="coupons"),
    path("", include("apps.qa.urls"), name="qa"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
