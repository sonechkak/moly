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


urlpatterns = [
    # Профиль
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
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
]
