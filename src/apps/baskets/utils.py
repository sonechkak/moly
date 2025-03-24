def add_product(basket_product):
    """Добавление количества товара в корзине."""
    basket_product.quantity += 1
    basket_product.save()
