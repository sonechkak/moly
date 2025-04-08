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


from django.http import HttpResponse


def hello(request):
    html = "<html><body>Hello world</body></html>"
    return HttpResponse(html)


urlpatterns = [
    # Профиль
    path(r"^profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path(r"^profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    # Адреса доставки
    path(r"^profile/<int:pk>/address/create/", ShippingAddressCreateView.as_view(), name="address-create"),
    path(
        r"^profile/<int:pk>/address/<int:address_pk>/update/",
        ShippingAddressUpdateView.as_view(),
        name="address-update",
    ),
    path(
        r"^profile/<int:pk>/address/<int:address_pk>/delete/",
        ShippingAddressDeleteView.as_view(),
        name="address-delete",
    ),
    path(
        r"^profile/<int:pk>/address/<int:address_pk>/set_primary/",
        ShippingAddressSetPrimaryView.as_view(),
        name="address-set-primary",
    ),
    path(r"^hello/", hello, name="hello"),
]
