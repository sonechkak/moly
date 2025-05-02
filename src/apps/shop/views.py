import logging

from apps.qa.forms import AnswerForm, QuestionForm
from apps.recommendations.services import RecommendationService
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, FormView, ListView

from .forms import ReviewForm
from .models import Category, Product, Review

User = get_user_model()
logger = logging.getLogger("user.actions")


class Index(ListView):
    """Главная страница."""

    model = Category
    context_object_name = "categories"
    template_name = "index/index.html"

    def get_queryset(self):
        categories = Category.objects.filter(parent__isnull=False)[:3]
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None

        products = self.get_top_products()

        # Рекомендации для авторизованных пользователей
        recommendations = RecommendationService.get_recommendations(user=user)[:6]

        context.update(
            {
                "title": "Главная страница",
                "products": products,
                "recommendations": recommendations,
            }
        )

        return context

    def get_top_products(self):
        """Возвращает топ-12 товара по количеству отзывов."""

        top_products = (
            Product.objects.filter(available=True)
            .annotate(reviews_count=Count("reviews"))
            .order_by("-reviews_count")[:12]
        )

        return top_products


class SubCategories(ListView):
    """Вывод подкатегорий."""

    model = Product
    context_object_name = "products"
    template_name = "shop/grid/shop.html"
    paginate_by = 12

    def get_queryset(self):
        """Вывод товаров определенной категории."""
        if type_field := self.request.GET.get("type"):
            return Product.objects.filter(category__slug=type_field)
        elif "slug" in self.kwargs:
            parent_category = get_object_or_404(Category, slug=self.kwargs["slug"])
            subcategories = parent_category.subcategories.all()

            products = (
                Product.objects.filter(category__in=subcategories)
                if subcategories.exists()
                else Product.objects.filter(category=parent_category)
            )
        else:
            products = Product.objects.filter(available=True)

        if sort_filed := self.request.GET.get("sort"):
            products = products.order_by(sort_filed)
        else:
            products = Product.objects.filter(id__in=products)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None

        if "slug" in self.kwargs:
            category = get_object_or_404(Category, slug=self.kwargs["slug"])
            context["title"] = f"Товары по категории: {category.title}"
        else:
            context["title"] = "Все товары"

        recommendations = RecommendationService.get_recommendations(user)[:6]
        context["recommendations"] = recommendations

        categories = Category.objects.filter(parent=None)
        context["categories"] = categories
        return context


class ProductDetail(DetailView):
    """Вывод информации о товаре."""

    model = Product
    context_object_name = "product"
    template_name = "shop/detalis/detail.html"

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user if self.request.user.is_authenticated else None

        RecommendationService.track_product_view(product, user)

        similar_products = RecommendationService.get_recommendations(user)
        reviews = Review.objects.filter(product=product).select_related("author").order_by("-created_at")

        context.update(
            {
                "title": product.title,
                "similar_products": similar_products,
                "reviews": reviews,
                "review_count": reviews.count(),
                "form": ReviewForm() if self.request.user.is_authenticated else None,
                "question_form": QuestionForm() if self.request.user.is_authenticated else None,
                "answers_form": AnswerForm() if self.request.user.is_authenticated else None,
            }
        )

        return context


class AddReviewView(LoginRequiredMixin, FormView):
    """Добавление отзыва."""

    form_class = ReviewForm

    def form_valid(self, form, **kwargs):
        review = form.save(commit=False)
        review.author = self.request.user
        product = Product.objects.get(pk=self.kwargs["pk"])
        review.product = product
        review.save()
        return redirect("shop:product_detail", slug=product.slug)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка добавления отзыва")
        return redirect("shop:product_detail", slug=self.kwargs["slug"])


class RemoveReviewView(LoginRequiredMixin, DeleteView):
    """Удаление отзыва."""

    model = Review
    login_url = "auth:login"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Отзыв успешно опубликован.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.kwargs["slug"]})
