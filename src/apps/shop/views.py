from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Category


class Index(ListView):
    """Главная страница."""
    model = Category
    template_name = "index/index.html"

    def get_queryset(self):
        """Вывод родительской категории."""
        return Category.objects.filter(parent=None).exclude(title="Все товары")[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["top_products"] = Product.objects.order_by("-watched")[:3]
        return context


class SubCategories(ListView):
    """Вывод подкатегорий."""
    model = Product
    context_object_name = "products"
    template_name = "shop/grid/shop-grid-left-sidebar-page.html"
    paginate_by = 12


    def get_queryset(self):
        """Вывод товаров определенной категории."""
        if type_field := self.request.GET.get("type"):
            return Product.objects.filter(category__slug=type_field)

        parent_category = get_object_or_404(Category, slug=self.kwargs["slug"])
        subcategories = parent_category.subcategories.all()

        # Если есть подкатегории, выбираем продукты из подкатегорий
        if subcategories.exists():
            products = Product.objects.filter(category__in=subcategories)
        else:
            # Если подкатегорий нет, выбираем продукты из самой категории
            products = Product.objects.filter(category=parent_category)

        if sort_filed := self.request.GET.get("sort"):
            products = products.order_by(sort_filed)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs["slug"])

        all_products_category = Category.objects.filter(title="Все товары").first()
        other_categories = Category.objects.exclude(title="Все товары").order_by("title")
        categories = [all_products_category] + list(other_categories)

        context["title"] = f"Товары по категории: {category.title}"
        context["category"] = Category.objects.get(slug=category.slug)
        context["categories"] = categories
        return context
