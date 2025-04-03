from apps.shop.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from .models import Basket, BasketProduct
from .utils import add_product


class AddToBasket(LoginRequiredMixin, View):
    """Вьюха для добавления товара в корзину."""

    login_url = "users:login_registration"

    def get(self, request, *args, **kwargs):
        """Добавление товара в корзину."""
        user = self.request.user
        product = get_object_or_404(Product, id=kwargs.get("pk"))
        basket, created = Basket.objects.get_or_create(user=user)
        basket.save()

        basket_product, created = BasketProduct.objects.get_or_create(product=product, basket=basket)
        basket_products = BasketProduct.objects.filter(basket=basket).all()

        if basket_product in basket_products:
            add_product(basket_product)

        next_page = request.META.get("HTTP_REFERER", None)
        return redirect(next_page)


class RemoveFromBasket(LoginRequiredMixin, View):
    """Вьюха для удаления товара из корзины."""

    def get(self, request, *args, **kwargs):
        user = self.request.user
        product = get_object_or_404(
            BasketProduct.objects.select_related("basket").filter(id=kwargs.get("pk"), basket__user=user)
        )
        product.delete()
        return redirect("baskets:basket")


class BasketView(LoginRequiredMixin, ListView):
    """Вьюха для корзины."""

    template_name = "shop/basket/basket.html"
    login_url = "users:login"

    def get_queryset(self):
        user = self.request.user
        basket, created = Basket.objects.get_or_create(user=user)
        return BasketProduct.objects.filter(basket=basket)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        basket = get_object_or_404(Basket, user=user)
        products = BasketProduct.objects.filter(basket=basket)

        if products.count() == 0:
            context["title"] = "Ваша корзина пуста!"
        else:
            context["title"] = "Корзина"

        context["basket"] = basket
        context["products"] = products
        return context
