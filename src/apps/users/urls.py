import pytz
from django.conf import settings
from django.urls import path

from .views import (
    ProfileUpdateView,
    ProfileView,
    ShippingAddressCreateView,
    ShippingAddressDeleteView,
    ShippingAddressSetPrimaryView,
    ShippingAddressUpdateView,
)

app_name = "users"

import datetime

from django.http import HttpResponse


def current_datetime(request):
    now = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)



urlpatterns = [
    # Профиль
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    # Адреса доставки
    path("profile/<int:pk>/address/create/", ShippingAddressCreateView.as_view(), name="address-create"),
    path(
        "profile/<int:pk>/address/<int:address_pk>/update/", ShippingAddressUpdateView.as_view(), name="address-update"
    ),
    path(
        "profile/<int:pk>/address/<int:address_pk>/delete/", ShippingAddressDeleteView.as_view(), name="address-delete"
    ),
    path(
        "profile/<int:pk>/address/<int:address_pk>/set_primary/",
        ShippingAddressSetPrimaryView.as_view(),
        name="address-set-primary",
    ),
    path("hello/", current_datetime, name="hello"),
]
