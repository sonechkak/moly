from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import FormView

from .forms import CouponForm
from .models import Coupon
from .utils.clear import clear_coupons_session


class CouponsView(LoginRequiredMixin, FormView):
    """Класс для отображения купонов."""

    form_class = CouponForm
    template_name = "shop/basket/basket.html"

    def form_valid(self, form):
        code = form.cleaned_data["coupon"]
        now = timezone.now()

        try:
            coupon = Coupon.objects.get(code__iexact=code, is_active=True, valid_from__lte=now, valid_to__gte=now)
            # Проверяем, не был ли купон уже использован
            if coupon.is_used:
                messages.error(self.request, "Купон уже использован.")
                clear_coupons_session(self.request)
                return self.form_invalid(form)
            # Проверяем пользователя, которому принадлежит купон
            if coupon.user and coupon.user != self.request.user:
                messages.error(self.request, "Этот купон предназначен для другого пользователя.")
                return self.form_invalid(form)
            # Проверяем, не истек ли срок действия купона
            if coupon.valid_to < now.date():
                messages.error(self.request, "Купон недействителен или истёк.")
                clear_coupons_session(self.request)
                return self.form_invalid(form)
            # Проверяем минимальную сумму заказа
            basket_total = self.request.user.basket.get_total_with_discount_and_cashback()
            if coupon.min_order_amount > basket_total:
                messages.error(
                    self.request,
                    f"Вам необходимо потратить {coupon.min_order_amount} рублей, чтобы использовать этот купон.",
                )
                return self.form_invalid(form)

            # Сохраняем необходимые данные купона
            self.request.session["coupon_id"] = coupon.id
            self.request.session["coupon_code"] = coupon.code
            self.request.session["coupon_discount"] = coupon.discount
            messages.success(self.request, f"Купон '{coupon.code}' успешно применён.")

        except Coupon.DoesNotExist:
            messages.error(self.request, "Купон недействителен или истёк.")
            clear_coupons_session(self.request)
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("baskets:basket", kwargs={"pk": self.request.user.pk})


class RemoveCouponsView(LoginRequiredMixin, View):
    """Класс для удаления купонов."""

    login_url = "auth:login"

    def get(self, request):
        if "coupon_id" in self.request.session:
            clear_coupons_session(self.request)
            messages.success(request, "Купон успешно удален.")
        return redirect(reverse("baskets:basket", kwargs={"pk": request.user.pk}))
