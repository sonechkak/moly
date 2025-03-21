from django.urls import path

from .views import (
    Index,
    SubCategories,
    ProductDetail,
    add_review,
    add_favorite,
    FavoriteProductsView,
    save_subscribers,
    send_mail_to_customers,
    basket, to_basket, checkout,
)


app_name = "shop"


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path('all_products/', SubCategories.as_view(), name='all_products'),
    path("category_list/<slug:slug>/", SubCategories.as_view(), name="category_list"),
    path("product_detail/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("review/<int:product_pk>", add_review, name="add_review"),
    path("add_favorite/<slug:product_slug>", add_favorite, name="add_favorite"),
    path("user_favorites/", FavoriteProductsView.as_view(), name="favorites"),
    path("subscribe/", save_subscribers, name="subscribe"),
    path("send_mail/", send_mail_to_customers, name="send_mail"),
    path("basket/", basket, name="basket"),
    path("to_basket/<int:product_id>/<str:action>/", to_basket, name="to_basket"),
    path("checkout/", checkout, name="checkout"),
]
