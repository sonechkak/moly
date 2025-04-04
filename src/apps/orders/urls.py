from django.urls import path

from .views import Checkout, OrderDetail

app_name = "orders"


urlpatterns = [
    path("checkout/<int:pk>/", Checkout.as_view(), name="checkout"),
    path("order_detail/<int:pk>/", OrderDetail.as_view(), name="order_detail"),
]
