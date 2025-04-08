from django.urls import path

from .views import (
    SaveSubscribers,
)

app_name = "subscribers"


urlpatterns = [
    path(r"^subscribe/", SaveSubscribers.as_view(), name="subscribe"),
]
