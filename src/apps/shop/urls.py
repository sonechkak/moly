from django.urls import include, path, re_path

from .views import Index, SubCategories


app_name = "shop"


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("category_list/<slug:slug>", SubCategories.as_view(), name="category_list"),
]
