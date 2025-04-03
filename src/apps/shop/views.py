from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import CustomerForm, ReviewForm
from .models import Category, Product
from .utils import get_random_products


class Index(ListView):
    """Главная страница."""

    model = Category
    template_name = "index/index.html"

    def get_queryset(self):
        """Вывод родительской категории."""
        return Category.objects.filter(parent=1)[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["products"] = Product.objects.order_by("-watched")[:12]
        return context


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

        if "slug" in self.kwargs:
            parent_category = get_object_or_404(Category, slug=self.kwargs["slug"])
            subcategories = parent_category.subcategories.all()

            # Если есть подкатегории, выбираем продукты из подкатегорий
            if subcategories.exists():
                products = Product.objects.filter(category__in=subcategories)
            else:
                # Если подкатегорий нет, выбираем продукты из самой категории
                products = Product.objects.filter(category=parent_category)

        else:
            products = Product.objects.filter(available=True)

        if sort_filed := self.request.GET.get("sort"):
            products = products.order_by(sort_filed)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "slug" in self.kwargs:
            category = get_object_or_404(Category, slug=self.kwargs["slug"])
            context["title"] = f"Товары по категории: {category.title}"
        else:
            context["title"] = "Все товары"

        categories = Category.objects.filter(parent=None)
        context["categories"] = categories
        return context


class ProductDetail(DetailView):
    """Вывод информации о товаре."""

    model = Product
    context_object_name = "product"
    template_name = "shop/detalis/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs["slug"])
        products = Product.objects.filter(category__in=product.category.all())
        context["title"] = product.title
        similar_products = get_random_products(product, products)
        context["similar_products"] = similar_products
        if self.request.user.is_authenticated:
            context["form"] = ReviewForm
        return context


def add_review(request, product_pk):
    """Сохранение отзыва."""
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_pk)
        review.product = product
        review.save()
        return redirect("shop:product_detail", slug=product.slug)
