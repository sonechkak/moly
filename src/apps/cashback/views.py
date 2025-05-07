from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView

from .forms import CashbackApplyForm


class CashbackApplyView(LoginRequiredMixin, FormView):
    """Вью для применения кэшбэка."""

    template_name = "shop/basket/basket.html"
    form_class = CashbackApplyForm

    def form_valid(self, form):
        cashback_used = form.cleaned_data["use_cashback"]
        self.request.session["use_cashback"] = cashback_used

        if cashback_used:
            cashback_amount = form.cleaned_data["cashback_amount"]
            self.request.session["cashback_amount"] = cashback_amount
            messages.success(self.request, "Кэшбэк успешно применен к заказу")
        else:
            messages.info(self.request, "Использование кэшбэка отменено")

        return super().form_valid(form)

    def get_success_url(self):
        # Возвращаем на страницу корзины
        return reverse("baskets:basket", kwargs={"pk": self.request.user.pk})

    def get_form_kwargs(self):
        """Добавляем начальное значение для чекбокса из сессии."""
        kwargs = super().get_form_kwargs()
        if "initial" not in kwargs:
            kwargs["initial"] = {}
        kwargs["initial"]["use_cashback"] = self.request.session.get("use_cashback", False)
        return kwargs
