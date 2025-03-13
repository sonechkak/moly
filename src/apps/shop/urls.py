from django.urls import include, path, re_path

from .views import Index, SubCategories, ProductDetail


app_name = "shop"


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("category_list/<slug:slug>/", SubCategories.as_view(), name="category_list"),
    path("product_detail/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
]
