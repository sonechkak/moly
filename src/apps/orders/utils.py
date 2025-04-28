from apps.baskets.models import BasketProduct
from apps.orders.models import Order, OrderProduct
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction


class OrderCreator(LoginRequiredMixin):
    """Класс для создания заказа."""

    @classmethod
    def create_order(cls, user, form_data, basket, request=None):
        """Создание заказа."""
        with transaction.atomic():
            if request:
                basket.bind_request(request)

            basket_products = BasketProduct.objects.filter(basket=basket)

            if not basket_products.exists():
                raise ValueError("Корзина пуста")

            address = (
                f"{form_data['city']}, "
                f"{form_data['state']}, "
                f"{form_data['street']} "
                f"{form_data['house']}, "
                f"{form_data['apartment']}"
            )

            order = Order.objects.create(
                customer=user.profile,
                is_paid=False,
                is_complete=False,
                is_shipping=True,
                payment_method=form_data["payment_method"],
                address=address,
                recipient=form_data["recipient"],
                contact=form_data["contact"],
                is_save_address=form_data["is_save_address"],
                total_cost=basket.get_total_with_discount,
            )

            for basket_product in basket_products:
                OrderProduct.objects.create(
                    order=order,
                    product=basket_product.product,
                    quantity=basket_product.quantity,
                    price=basket_product.get_total_price,
                )

            return order
