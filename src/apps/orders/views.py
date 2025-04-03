from apps.baskets.models import Basket, BasketProduct
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, FormView
from utils.order_creator import OrderCreator

from .forms import ShippingForm
from .models import Order


class Checkout(LoginRequiredMixin, FormView):
    """Вьюха для оформления заказа."""

    form_class = ShippingForm
    model = Order
    template_name = "shop/basket/checkout.html"
    success_url = "/checkout/success/"

    def get_queryset(self):
        user = self.request.user
        products = BasketProduct.objects.filter(basket__user=user)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        context["basket_products"] = BasketProduct.objects.filter(basket__user=self.request.user).select_related(
            "product"
        )
        context["basket"] = get_object_or_404(Basket, user=self.request.user)
        return context

    def form_valid(self, form):
        try:
            order = OrderCreator.create_order(
                user=self.request.user,
                form_data=form.cleaned_data,
            )
            messages.success(self.request, "Ваш заказ успешно оформлен!")
            return redirect("orders:order_detail", pk=order.pk)
        except ValueError as e:
            form.add_error(None, e)
            return self.form_invalid(form)


class OrderDetail(LoginRequiredMixin, DetailView):
    """Вьюха для детального заказа."""

    model = Order
    template_name = "shop/basket/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error()
