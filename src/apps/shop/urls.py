from django.urls import path

from .views import (
    AddReviewView,
    Index,
    ProductDetail,
    SubCategories,
)

app_name = "shop"


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path(r"^all_products/", SubCategories.as_view(), name="all_products"),
    path(r"^category_list/<slug:slug>/", SubCategories.as_view(), name="category_list"),
    path(r"^product_detail/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path(r"^review/<int:pk>", AddReviewView.as_view(), name="add_review"),
]
