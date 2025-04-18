from django.contrib import messages
from django.core.cache import caches
from django.db.models import Count, F
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, ListView

from .forms import ReviewForm
from .models import Category, Product, Review
from .utils import get_random_products

cache = caches["default"]


class Index(ListView):
    """Главная страница."""

    model = Category
    context_object_name = "categories"
    template_name = "index/index.html"

    def get_queryset(self):
        """Вывод родительской категории."""
        cache_key = "parent_categories"
        categories = cache.get(cache_key)

        if not categories:
            categories = Category.objects.filter(parent=1)[:3]
            cache.set(cache_key, categories, 60 * 15)

        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = "top_products"
        products = cache.get(cache_key)

        if not products:
            products = self.get_top_products()
            cache.set(cache_key, products, 60 * 15)

        context.update(
            {
                "title": "Главная страница",
                "products": products,
            }
        )

        return context

    def get_top_products(self):
        """Возвращает топ-12 товара по количеству отзывов."""
        cache_key = "top_products_by_reviews"
        top_products = cache.get(cache_key)

        if not top_products:
            top_products = (
                Product.objects.filter(available=True)
                .annotate(reviews_count=Count("reviews"))
                .order_by("-reviews_count")[:12]
            )

            cache.set(cache_key, top_products, 60 * 15)

        return top_products


class SubCategories(ListView):
    """Вывод подкатегорий."""

    model = Product
    context_object_name = "products"
    template_name = "shop/grid/shop.html"
    paginate_by = 12

    def get_queryset(self):
        """Вывод товаров определенной категории."""
        cache_key = "subcategories_page_products"
        products = cache.get(cache_key)

        if not products:
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
                cache.set(cache_key, list(products.values_list("id", flat=True)), 60 * 15)

        else:
            products = Product.objects.filter(id__in=products)

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

    def get_object(self, queryset=None):
        cache_key = f"product_{self.kwargs['slug']}"
        product = cache.get(cache_key)

        if not product:
            product = get_object_or_404(Product, slug=self.kwargs["slug"])
            cache.set(cache_key, product, 60 * 15)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        slug = self.kwargs["slug"]

        cache_key_similar = f"similar_products_{slug}"
        similar_products = cache.get(cache_key_similar)

        if not similar_products:
            products = Product.objects.filter(category__in=product.category.all())
            similar_products = get_random_products(product, products)
            cache.set(cache_key_similar, similar_products, 60 * 15)

        cache_key_reviews = f"reviews_{slug}"
        reviews = cache.get(cache_key_reviews)

        if not reviews:
            reviews = Review.objects.filter(product=product).select_related("author").order_by("-created_at")
            cache.set(cache_key_reviews, reviews, 60 * 15)

        context.update(
            {
                "title": product.title,
                "similar_products": similar_products,
                "reviews": reviews,
                "review_count": len(reviews),
                "form": ReviewForm() if self.request.user.is_authenticated else None,
            }
        )

        return context


class AddReviewView(FormView):
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
