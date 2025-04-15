from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import ShippingForm
from .models import Profile, ShippingAddress


class ProfileView(LoginRequiredMixin, DetailView):
    """Профиль пользователя."""

    model = Profile
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Профиль пользователя: {self.request.user.username}"
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["avatar", "first_name", "last_name", "phone", "email"]
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование профиля"
        return context

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.object.pk})


class ShippingAddressCreateView(LoginRequiredMixin, CreateView):
    model = ShippingAddress
    form_class = ShippingForm
    template_name = "users/address-create.html"

    def form_valid(self, form):
        result = super().form_valid(form)
        form.instance.customer = Profile.objects.get(user=self.request.user)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление адреса доставки"
        return context

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})


class ShippingAddressSetPrimaryView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(Profile, user=self.request.user)
        address = get_object_or_404(ShippingAddress, pk=self.kwargs.get("address_pk"), customer__user=user)
        ShippingAddress.objects.filter(customer__user=user, is_primary=True).update(is_primary=False)

        address.is_primary = True
        address.save()

        return redirect(reverse_lazy("users:profile", kwargs={"pk": user.pk}))


class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    model = ShippingAddress
    form_class = ShippingForm
    template_name = "users/address-update.html"
    context_object_name = "address"

    def get_object(self, queryset=None):
        address_id = self.kwargs.get("address_pk")
        return get_object_or_404(ShippingAddress, pk=address_id, customer__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление адреса доставки из профиля."""

    model = ShippingAddress
    context_object_name = "address"

    def get_object(self, queryset=...):
        user = self.request.user
        return get_object_or_404(ShippingAddress, pk=self.kwargs.get("address_pk"), customer_id=user.pk)

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})
