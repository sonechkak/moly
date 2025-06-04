import logging

from apps.notifications.models import Notification, ProductAvalaibilityNotification
from apps.notifications.services.get_unread_count import get_unread_count
from apps.qa.forms import AnswerForm, QuestionForm
from apps.recommendations.services import RecommendationService, YouWatchedService
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
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

        # Вы смотрели
        viewed_products = YouWatchedService.get_watched_products(user=user)[:6]

        context.update(
            {
                "title": "Главная страница",
                "products": products,
                "recommendations": recommendations,
                "viewed_products": viewed_products,
                "unread_notifications_count": get_unread_count(user=user),
                "notifications": Notification.objects.filter(user=user)[:6],
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

        if sort_field := self.request.GET.get("sort"):
            products = products.order_by(sort_field)

        if cpu_types := self.request.GET.getlist("cpu_type"):
            products = products.filter(cpu_type__in=cpu_types)

        if ram_sizes := self.request.GET.getlist("ram"):
            products = products.filter(ram__in=ram_sizes)

        if storage_sizes := self.request.GET.getlist("storage"):
            products = products.filter(storage__in=storage_sizes)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        recommendations = RecommendationService.get_recommendations(user)[:6]
        categories = Category.objects.filter(parent=None)

        if "slug" in self.kwargs:
            category = get_object_or_404(Category, slug=self.kwargs["slug"])
            context["title"] = f"Товары по категории: {category.title}"
        else:
            context["title"] = "Все товары"

        context.update(
            {
                "recommendations": recommendations,
                "categories": categories,
                "products_count": Product.objects.all().count(),
                "unread_notifications_count": get_unread_count(user=user),
                "notifications": Notification.objects.filter(user=user)[:6],
            }
        )
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

        similar_products = RecommendationService._get_similar_products_for_product(product, limit=6)
        reviews = product.reviews.all().order_by("-created_at")

        # Обновляем просмотры пользователя
        YouWatchedService.update_watched_page(user=user, product=product)

        is_subscribed = False
        if user:
            is_subscribed = ProductAvalaibilityNotification.objects.filter(user=user, product=product).exists()

        context.update(
            {
                "title": product.title,
                "similar_products": similar_products,
                "reviews": reviews,
                "review_count": reviews.count(),
                "is_subscribed": is_subscribed,
                "unread_notifications_count": get_unread_count(user=user),
                "notifications": Notification.objects.filter(user=user)[:6],
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


class ComparisonListView(ListView):
    """Страница списка товаров для сравнения."""

    model = Product
    template_name = "shop/compare/compare.html"
    context_object_name = "products"

    def get_queryset(self):
        """Получаем список товаров для сравнения из сессии или GET-параметров."""
        product_ids = self.request.GET.getlist("compare_products")

        if not product_ids:
            product_ids = self.request.session.get("compare_products", [])
        else:
            product_ids = [int(pid) for pid in product_ids if pid.isdigit()]
            self.request.session["compare_products"] = product_ids

        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            products_dict = {p.id: p for p in products}
            return [products_dict[pid] for pid in product_ids if pid in products_dict]

        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = self.request.session.get("compare_products", [])
        context["compare_count"] = len(context["products"])
        context["max_compare_items"] = 4
        context["compare_product_ids"] = product_ids
        return context


class AddToCompareView(LoginRequiredMixin, View):
    """Добавление товара в сравнение."""

    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs.get("pk"), available=True)
        except Product.DoesNotExist:
            messages.error(request, "Товар не найден или недоступен.")
            return redirect(request.META.get("HTTP_REFERER", "shop:all_products"))

        product_ids = request.session.get("compare_products", [])
        max_items = 4

        if len(product_ids) >= max_items and product.id not in product_ids:
            messages.warning(request, f"Вы можете сравнивать не более {max_items} товаров одновременно.")
            return redirect(
                request.META.get("HTTP_REFERER") or reverse("shop:product_detail", kwargs={"slug": product.slug})
            )

        if product.id not in product_ids:
            product_ids.append(product.id)
            request.session["compare_products"] = product_ids
            messages.success(request, f"{product.title} добавлен в сравнение.")
        else:
            messages.info(request, f"{product.title} уже добавлен в сравнение.")

        return redirect(request.META.get("HTTP_REFERER") or "shop:comparison_list")


class RemoveFromCompareView(LoginRequiredMixin, View):
    """Удаление товара из сравнения."""

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Товар не найден.")
            return redirect("shop:compare_list")

        product_ids = request.session.get("compare_products", [])

        if product.id in product_ids:
            product_ids.remove(product.id)
            request.session["compare_products"] = product_ids
            messages.success(request, f"{product.title} удален из сравнения.")
        else:
            messages.info(request, f"{product.title} не найден в сравнении.")

        return redirect(request.META.get("HTTP_REFERER", "shop:compare_list"))


class CompareProductsView(LoginRequiredMixin, ListView):
    """Сравнение товаров."""

    model = Product
    context_object_name = "products"
    template_name = "shop/compare/compare.html"

    def get_queryset(self):
        product_ids = self.request.GET.getlist("product_ids")
        return Product.objects.filter(id__in=product_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Сравнение товаров"
        context["unread_notifications_count"] = get_unread_count(user=self.request.user)
        context["notifications"] = Notification.objects.filter(user=self.request.user)[:6]
        return context
