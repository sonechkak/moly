from django.urls import path

from .views import (
    FavoriteProductsView,
    add_favorite,
)

app_name = "favs"


urlpatterns = [
    path("add_favorite/<slug:product_slug>", add_favorite, name="add_favorite"),
    path("user_favorites/", FavoriteProductsView.as_view(), name="favorites"),
]
