import stripe
from apps.baskets.models import Basket, BasketProduct
from apps.cashback.models import CashbackBalance
from apps.cashback.utils.create_cashback import create_cashback
from apps.coupons.models import Coupon
from apps.coupons.utils.clear import clear_coupons_session
from apps.loyalty.utils.add_cashback import update_cashback_balance
from apps.stripe_app.utils import handle_stripe_payment
from apps.users.models import Profile
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import OrderForm
from .models import Order
from .utils import OrderCreator

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserOrders(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "orders/user_orders.html"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_orders"] = self.get_queryset().count()
        context["total_spent"] = sum(order.total_cost for order in context["orders"] if order.payment_status == "paid")
        context["status_choices"] = Order.PAYMENT_STATUS_CHOICES

        return context


class Checkout(LoginRequiredMixin, FormView):
    """Вью для оформления заказа."""

    form_class = OrderForm
    template_name = "shop/basket/checkout.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        user = self.request.user
        products = BasketProduct.objects.filter(basket__user=user)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        context["basket_products"] = BasketProduct.objects.filter(basket__user=self.request.user).select_related(
            "product"
        )

        basket = get_object_or_404(Basket, user=self.request.user)
        basket.bind_request(self.request)
        context["basket"] = basket
        return context

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = self.request.user
        basket = get_object_or_404(Basket, user=user)

        self.order = OrderCreator.create_order(
            user=user,
            form_data=form_data,
            basket=basket,
            cashback_used=self.request.session.get("use_cashback", False),
            cashback_amount=self.request.session.get("cashback_amount", 0),
            coupon_used=self.request.session.get("coupon_id", False),
            request=self.request,
        )

        if form.cleaned_data["payment_method"] == "card_online":
            return handle_stripe_payment(self, self.order)

        return super().form_valid(form)

    def form_invalid(self, form):
        result = super().form_invalid(form)
        for error in form.errors:
            messages.error(self.request, form.errors[error].as_text())
        return result

    def get_success_url(self):
        if self.order:
            return reverse("orders:order_detail", kwargs={"pk": self.order.pk})
        return reverse("orders:checkout", kwargs={"pk": self.user.pk})


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


class PaymentSuccess(LoginRequiredMixin, TemplateView):
    template_name = "orders/payment_success.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(Order, pk=order_id, customer=request.user.profile)

        try:
            session = stripe.checkout.Session.retrieve(order.stripe_session_id)

            if session.payment_status == "paid":
                order.is_paid = True
                order.payment_status = "paid"
                order.payment_method = "card_online"
                order.stripe_session_id = session.id
                order.save(update_fields=["is_paid", "payment_status", "payment_method", "stripe_session_id"])

                if order.cashback_used:
                    cashback_balance = CashbackBalance.objects.get(user=request.user)
                    cashback_balance.total = 0
                    cashback_balance.save(update_fields=["total"])

                    if "use_cashback" in request.session:
                        del request.session["use_cashback"]

                # Создаем кэшбэк для пользователя
                create_cashback(request, user=request.user, order=order)

                # Обновляем баланс кэшбэка
                update_cashback_balance(request, user=request.user, order=order)

                coupon_code = self.request.session.get("coupon_code")
                if coupon_code:
                    coupon = Coupon.objects.get(code=coupon_code)
                    if coupon.user:
                        coupon.delete()
                    clear_coupons_session(self.request)

                # Очищаем корзину
                basket_products = BasketProduct.objects.filter(basket__user=request.user)
                basket_products.delete()

                messages.success(request, "Платеж успешно завершен! Ваш заказ обрабатывается.")
            else:
                messages.warning(request, "Платеж еще не подтвержден. Мы уведомим вас, когда платеж будет получен.")

        except stripe.error.StripeError:
            messages.error(request, "Ошибка при проверке статуса платежа. Пожалуйста, свяжитесь с поддержкой.")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get("pk")
        context["order"] = get_object_or_404(Order, pk=order_id, customer=self.request.user.profile)
        return context


class PaymentCancel(LoginRequiredMixin, TemplateView):
    template_name = "orders/payment_cancel.html"

    def get(self, request, *args, **kwargs):
        messages.info(request, "Вы можете попробовать оплатить заказ еще раз.")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get("pk")
        context["order"] = get_object_or_404(Order, pk=order_id, customer=self.request.user.profile)
        context["retry_url"] = reverse("orders:checkout")
        return context
