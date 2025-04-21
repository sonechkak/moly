from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    AddReviewView,
    Index,
    ProductDetail,
    SubCategories,
)

app_name = "shop"


urlpatterns = [
    path("", cache_page(60 * 15)(Index.as_view()), name="index"),
    path("all_products/", cache_page(60 * 15)(SubCategories.as_view()), name="all_products"),
    path("category_list/<slug:slug>/", cache_page(60 * 15)(SubCategories.as_view()), name="category_list"),
    path("product_detail/<slug:slug>/", cache_page(60 * 15)(ProductDetail.as_view()), name="product_detail"),
    path("review/<int:pk>", AddReviewView.as_view(), name="add_review"),
]
