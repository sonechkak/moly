from django.http import HttpResponse
from django.urls import path, re_path

from .views import *

app_name = "users"


def hello(request):
    html = "<html><body>Hello world</body></html>"
    return HttpResponse(html)


urlpatterns = [
    # Профиль
    re_path(r"^profile/<int:pk>", ProfileView.as_view(), name="profile"),
    re_path(r"^profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    # Адреса доставки
    re_path(r"^profile/<int:pk>/address/create/", ShippingAddressCreateView.as_view(), name="address-create"),
    re_path(
        r"^profile/<int:pk>/address/<int:address_pk>/update/",
        ShippingAddressUpdateView.as_view(),
        name="address-update",
    ),
    re_path(
        r"^profile/<int:pk>/address/<int:address_pk>/delete/",
        ShippingAddressDeleteView.as_view(),
        name="address-delete",
    ),
    re_path(
        r"^profile/<int:pk>/address/<int:address_pk>/set_primary/",
        ShippingAddressSetPrimaryView.as_view(),
        name="address-set-primary",
    ),
    re_path(r"^hello/", hello, name="hello"),
]
