from django.urls import path

from .views import *

app_name = "baskets"


urlpatterns = [
    path(r"^basket/<int:pk>/", BasketView.as_view(), name="basket"),
    path(r"^to_basket/<int:pk>/", AddToBasket.as_view(), name="to_basket"),
    path(r"^from_basket/<int:pk>/", RemoveFromBasket.as_view(), name="from_basket"),
]
