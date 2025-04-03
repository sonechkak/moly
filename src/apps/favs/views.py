from apps.favs.models import FavoriteProducts
from apps.shop.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView


class FavoriteProductsView(LoginRequiredMixin, ListView):
    """Страница избранных товаров."""

    model = FavoriteProducts
    context_object_name = "products"
    template_name = "shop/favorite_products/favorite_products.html"
    login_url = "auth:login_registration"
    paginate_by = 12

    def get_queryset(self):
        """Получаем избранные товары для пользователя."""
        favs = FavoriteProducts.objects.filter(user=self.request.user)
        products = [i.product for i in favs]
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранные товары"
        return context


def add_favorite(request, product_slug):
    """Добавление или удаление товара из избранного."""
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=product_slug)
        query_products = FavoriteProducts.objects.filter(user=user)
        if product in [i.product for i in query_products]:
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=user, product=product)

        next_page = request.META.get("HTTP_REFERER", None)

        return redirect(next_page)
