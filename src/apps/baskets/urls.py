from django.urls import path

from .views import (
    BasketView,
    AddToBasket,
    RemoveFromBasket,
    Checkout
)


app_name = "baskets"


urlpatterns = [
    path("basket/", BasketView.as_view(), name="basket"),
    path("to_basket/<int:pk>/", AddToBasket.as_view(), name="to_basket"),
    path("from_basket/<int:pk>/", RemoveFromBasket.as_view(), name="from_basket"),
    path("checkout/", Checkout.as_view(), name="checkout"),
]
