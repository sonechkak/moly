from django.urls import path

from .views import CouponsView, RemoveCouponsView

app_name = "coupons"


urlpatterns = [
    path("apply-coupon/", CouponsView.as_view(), name="apply"),
    path("remove-coupon/", RemoveCouponsView.as_view(), name="remove"),
]
