from django.urls import path

from .views import (
    AddToFavoriteProducts,
    FavoriteProductsView,
)

app_name = "favs"


urlpatterns = [
    path(r"^add_favorite/<slug:slug>", AddToFavoriteProducts.as_view(), name="add_favorite"),
    path(r"^user_favorites/", FavoriteProductsView.as_view(), name="favorites"),
]
