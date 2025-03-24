from django.urls import path

from .views import (
    Index,
    SubCategories,
    ProductDetail,
    add_review,
)


app_name = "shop"


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path('all_products/', SubCategories.as_view(), name='all_products'),
    path("category_list/<slug:slug>/", SubCategories.as_view(), name="category_list"),
    path("product_detail/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("review/<int:product_pk>", add_review, name="add_review"),
]
