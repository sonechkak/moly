from django.urls import path

from .views import (
    AddReviewView,
    AddToCompareView,
    ComparisonListView,
    DeleteSearchHistoryView,
    Index,
    ProductDetail,
    RemoveFromCompareView,
    RemoveReviewView,
    SearchHistoryView,
    SearchView,
    SubCategories,
)

app_name = "shop"

urlpatterns = [
    # Products and categories
    path("", Index.as_view(), name="index"),
    path("all_products/", SubCategories.as_view(), name="all_products"),
    path("category_list/<slug:slug>/", SubCategories.as_view(), name="category_list"),
    path("product_detail/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    # Search
    path("search/", SearchView.as_view(), name="search"),
    path("search/history/", SearchHistoryView.as_view(), name="search_history"),
    path("search/history/delete", DeleteSearchHistoryView.as_view(), name="search_delete"),
    # Comparison views
    path("compare/", ComparisonListView.as_view(), name="compare_list"),
    path("compare/<int:pk>/add/", AddToCompareView.as_view(), name="add_compare"),
    path("compare/<int:pk>/remove/", RemoveFromCompareView.as_view(), name="remove_compare"),
    # Reviews
    path("review/<int:pk>/add/", AddReviewView.as_view(), name="add_review"),
    path("review/<int:pk>/remove/", RemoveReviewView.as_view(), name="remove_review"),
]

# urlpatterns = [
#     path("", cache_page(60 * 15)(Index.as_view()), name="index"),
#     path("all_products/", cache_page(60 * 15)(SubCategories.as_view()), name="all_products"),
#     path("category_list/<slug:slug>/", cache_page(60 * 15)(SubCategories.as_view()), name="category_list"),
#     path("product_detail/<slug:slug>/", cache_page(60 * 15)(ProductDetail.as_view()), name="product_detail"),
#     path("review/<int:pk>/add/", AddReviewView.as_view(), name="add_review"),
#     path("review/<int:pk>/remove/", RemoveReviewView.as_view(), name="remove_review"),
# ]
