from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.shop.urls"), name="shop"),
    path("", include("apps.auth.urls"), name="auth"),
    path("", include("apps.baskets.urls"), name="baskets"),
    path("", include("apps.favs.urls"), name="favs"),
    path("", include("apps.orders.urls"), name="orders"),
    path("", include("apps.subscribers.urls"), name="subscribers"),
    path("", include("apps.users.urls"), name="users"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
