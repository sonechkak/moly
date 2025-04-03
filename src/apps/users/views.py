from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView, UpdateView

from .models import Profile


class ProfileView(LoginRequiredMixin, DetailView):
    """Профиль пользователя."""

    model = Profile
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context["title"] = f"Профиль пользователя: {user.username}"
        return context


class ProfileUpdateView(UpdateView):
    pass
