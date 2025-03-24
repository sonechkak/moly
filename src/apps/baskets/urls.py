from django.urls import path

from .views import (
    basket,
    to_basket,
    checkout,
)


app_name = "baskets"


urlpatterns = [
    path("basket/", basket, name="basket"),
    path("to_basket/<int:product_id>/<str:action>/", to_basket, name="to_basket"),
    path("checkout/", checkout, name="checkout"),
]
