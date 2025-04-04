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
    path("all_products/", SubCategories.as_view(), name="all_products"),
    path("category_list/<slug:slug>/", SubCategories.as_view(), name="category_list"),
    path("product_detail/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("review/<int:pk>", AddReviewView.as_view(), name="add_review"),
]
