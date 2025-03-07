from django.urls import include, path, re_path

from .views import Index


app_name = "shop"


urlpatterns = [
    path("", Index.as_view(), name="index"),
]
