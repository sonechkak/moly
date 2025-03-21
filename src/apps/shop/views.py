from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from .models import Product, Category, FavoriteProducts, Mail
from .utils import get_random_products
from .forms import ReviewForm


class Index(ListView):
    """Главная страница."""
    model = Category
    template_name = "index/index.html"

    def get_queryset(self):
        """Вывод родительской категории."""
        return Category.objects.filter(parent=None)[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["products"] = Product.objects.order_by("-watched")
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
        return redirect('shop:product_detail', slug=product.slug)


def add_favorite(request, product_slug):
    """Добавление или удаление товара с избранного."""
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=product_slug)
        query_products = FavoriteProducts.objects.filter(user=user)
        if product in [i.product for i in query_products]:
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=user, product=product)

        next_page = request.META.get("HTTP_REFERER", None)

        return redirect(next_page)


class FavoriteProductsView(LoginRequiredMixin, ListView):
    """Страница с избранными товарами."""
    model = FavoriteProducts
    context_object_name = "products"
    template_name = "shop/favorite_products/favorite_products.html"
    login_url = "auth:login_registration"
    paginate_by = 12

    def get_queryset(self):
        """Получаем избранные товары для пользователя."""
        favs = FavoriteProducts.objects.filter(user=self.request.user)
        products =  [i.product for i in favs]
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранные товары"
        return context


def save_subscribers(request):
    """Собирает почтовые адреса."""
    email = request.POST.get("email")
    user = request.user if request.user.is_authenticated else None
    if email:
        try:
            Mail.objects.create(email=email, user=user)
        except IntegrityError:
            messages.error(request, "Вы уже подписались на новости.")

    return redirect("shop:index")


def send_mail_to_customers(request):
    """Отправка сообщений подписчикам."""
    from conf import settings
    from django.core.mail import send_mail

    if request.method == "POST":
        text = request.POST.get("text")
        mail_list = Mail.objects.all()
        for email in mail_list:
            send_mail(
                subject="У вас новая акция",
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email.email],
                fail_silently=False,
            )
            print(f"Сообщения отправлено на почту: {email.email} ----- {bool(send_mail)}")

    context = {"title": "Спамер"}
    return render(request, "shop/send_mail.html", context)
