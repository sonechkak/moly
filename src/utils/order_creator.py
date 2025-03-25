from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect

from apps.baskets.models import BasketProduct
from apps.orders.models import Order, OrderProduct


class OrderCreator(LoginRequiredMixin):
    """Класс для создания заказа."""

    def __init__(self, user, products):
        self.user = user
        self.products = products

    @classmethod
    def create_order(cls, user, form_data):
        """Создание заказа."""
        # Все операции в одной транзакции
        with transaction.atomic():
            # Добавляем профиль и корзину
            profile = user.profile
            basket_products = BasketProduct.objects.filter(basket__user=user).select_related('product')

            if not basket_products.exists():
                raise ValueError("Корзина пуста")

            order = Order.objects.create(
                customer=profile,
                is_complete=False,
                is_shipping=form_data['is_shipping'],
                address=form_data['address'],
                recipient=form_data['recipient'],
                contact=form_data['contact'],
                is_paid=False,
                total_cost=profile.basket.basket_total_cost,
                total_price=profile.basket.basket_total_price,
            )

            order_products = [
                OrderProduct(
                    order=order,
                    product=product.product,
                    quantity=product.quantity,
                    price=product.get_total_price,
                )
                for product in basket_products
            ]

            OrderProduct.objects.bulk_create(order_products)
            basket_products.delete()
            return order