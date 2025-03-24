from random import randint
from .models import (
    Product,
)


def get_random_products(product, products):
    data = []
    for i in range(6):
        random_index = randint(0, len(products) - 1)
        random_item = products[random_index]
        if random_item not in data and str(random_item) != product.title:
            data.append(random_item)

    return data


class BasketForAuthenticatedUser:
    """Логика для корзины."""
    def __init__(self, request):
        pass

    def get_cate_info(self):
        """Получение информации о корзине (кол-во и сумма товаров) и заказчике."""
        pass

    def add_or_delete(self, product_id, action):
        """Добавление и удаление товара по нажатию на плюс и минус."""
        pass


def get_basket_data(request):
    """Вывод товаров с корзины на страницу."""
    pass
