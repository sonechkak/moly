from django.urls import path

from .views import AddToBasket, BasketView, RemoveFromBasket

app_name = "baskets"


urlpatterns = [
    path("basket/<int:pk>/", BasketView.as_view(), name="basket"),
    path("to_basket/<int:pk>/", AddToBasket.as_view(), name="to_basket"),
    path("from_basket/<int:pk>/", RemoveFromBasket.as_view(), name="from_basket"),
]
