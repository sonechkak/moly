from django.urls import path

from .views import Checkout, OrderDetail, PaymentCancel, PaymentSuccess, UserOrders

app_name = "orders"


urlpatterns = [
    path("all_orders/<int:pk>/", UserOrders.as_view(), name="my_orders"),
    path("checkout/<int:pk>/", Checkout.as_view(), name="checkout"),
    path("order_detail/<int:pk>/", OrderDetail.as_view(), name="order_detail"),
    path("payment/<int:pk>/success/", PaymentSuccess.as_view(), name="payment_success"),
    path("payment/<int:pk>/cancel/", PaymentCancel.as_view(), name="payment_cancel"),
]
