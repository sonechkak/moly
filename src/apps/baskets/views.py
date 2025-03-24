from django.shortcuts import render, redirect


def to_basket(request, product_id, action):
    """Для добавления товара в корзину."""
    if request.user.is_authenticated:
        user = request.user

    next_page = request.META.get("HTTP_REFERER", None)
    return redirect(next_page)


def basket(request):
    """Страница корзины."""
    context = {"title": "Корзина"}
    return render(request, 'shop/basket/basket.html', context)


def checkout(request):
    """Страница оформления заказа."""
    return render(request, 'shop/basket/checkout.html')

