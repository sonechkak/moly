from itertools import product

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from .models import OrderProduct, Order
from ..baskets.models import BasketProduct


class Checkout(LoginRequiredMixin, ListView):
    """Вьюха для оформления заказа."""
    model = OrderProduct
    context_object_name = "products"
    login_url = "users:login_registration"
    template_name = "shop/basket/checkout.html"

    def get_queryset(self):
        user = self.request.user
        products = BasketProduct.objects.filter(basket__user=user)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = OrderProduct.objects.filter(basket__user=self.request.user)
        context["title"] = "Оформление заказа"
        context["total_sum"] = sum([item.get_total_price for item in product_list])
        return context
