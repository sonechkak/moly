from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .models import FavoriteProducts, Product


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


class AddToFavoriteProducts(LoginRequiredMixin, View):
    """Добавление товара в избранное."""

    def get(self, request, *args, **kwargs):
        """Добавление товара в избранное."""
        user = self.request.user
        product = get_object_or_404(Product, slug=kwargs["slug"])

        query_products = FavoriteProducts.objects.filter(user=user)

        if product in [i.product for i in query_products]:
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            fav_product = FavoriteProducts.objects.create(user=user, product=product)

        next_page = self.request.META.get("HTTP_REFERER", None)
        return redirect(next_page)
