from apps.shop.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Answer, Question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания вопроса пользователя."""

    template_name = "shop/detalis/_components/_questions.html"
    model = Question
    fields = ("text",)

    def get_success_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.kwargs["slug"]})

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.text = form.cleaned_data["text"]
        product = Product.objects.get(slug=self.kwargs["slug"])
        question.product = product
        question.save()
        messages.success(self.request, "Ваш вопрос успешно опубликован.")
        return super().form_valid(form)


class QuestionRemoveView(LoginRequiredMixin, DeleteView):
    """Класс для удаления вопроса пользователя."""

    model = Question
    login_url = "auth:login"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Отзыв успешно удален.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.kwargs["slug"]})


class AnswerCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания ответа на вопрос пользователя."""

    template_name = "shop/detalis/_components/_questions.html"
    fields = ("text",)
    model = Answer

    def get_success_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.kwargs["slug"]})

    def form_valid(self, form):
        answer = form.save(commit=False)
        question = Question.objects.get(pk=self.kwargs["pk"])
        answer.user = self.request.user
        answer.text = form.cleaned_data["text"]
        answer.product = question.product
        answer.question = question
        question.save()
        messages.success(self.request, "Ваш ответ успешно опубликован.")
        return super().form_valid(form)


class AnswerRemoveView(LoginRequiredMixin, DeleteView):
    """Класс для удаления вопроса пользователя."""

    model = Answer
    login_url = "auth:login"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Ответ успешно удален.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.kwargs["slug"]})


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования ответа на вопрос пользователя."""

    template_name = "shop/detalis/_components/_answer_form.html"
    fields = ("text",)
    model = Answer

    def get_success_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.kwargs["slug"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(slug=self.kwargs["slug"])
        return context
