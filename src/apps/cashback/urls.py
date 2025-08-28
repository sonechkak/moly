from django.urls import path

from .views import CashbackApplyView

app_name = "cashback"


urlpatterns = [
    path("cashback/", CashbackApplyView.as_view(), name="apply"),
]
