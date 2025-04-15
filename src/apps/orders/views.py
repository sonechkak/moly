from apps.baskets.models import Basket, BasketProduct
from apps.users.forms import ShippingForm
from apps.users.models import Profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, FormView
from utils.order_creator import OrderCreator

from .models import Order


class Checkout(LoginRequiredMixin, FormView):
    """Вью для оформления заказа."""

    form_class = ShippingForm
    template_name = "shop/basket/checkout.html"

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
        result = super().form_valid(form)
        basket = get_object_or_404(Basket, user=self.request.user)
        OrderCreator.create_order(
            user=self.request.user,
            form_data=form.cleaned_data,
            basket=basket,
        )
        messages.success(self.request, "Ваш заказ успешно оформлен!")
        return result

    def form_invalid(self, form):
        result = super().form_invalid(form)
        messages.error(self.request, "Ошибка оформления заказа. Проверьте введенные данные.")
        return result

    def get_success_url(self):
        return redirect("orders:order_detail", pk=self.object.pk)


class OrderDetail(LoginRequiredMixin, DetailView):
    """Вью для детального заказа."""

    model = Order
    template_name = "shop/basket/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        customer = Profile.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Детали заказа: {self.object.id}"
        return context
