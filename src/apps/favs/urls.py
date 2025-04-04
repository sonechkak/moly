from django.urls import path

from .views import (
    AddToFavoriteProducts,
    FavoriteProductsView,
)

app_name = "favs"


urlpatterns = [
    path("add_favorite/<slug:slug>", AddToFavoriteProducts.as_view(), name="add_favorite"),
    path("user_favorites/", FavoriteProductsView.as_view(), name="favorites"),
]
