from decimal import Decimal

from apps.cashback.models import CashbackBalance
from apps.coupons.models import Coupon
from apps.shop.models import Product
from django.contrib.auth import get_user_model
from django.db import models
from utils.db import TimeStamp

user_model = get_user_model()


class Basket(TimeStamp, models.Model):
    """Корзина товаров."""

    user = models.OneToOneField(
        user_model, on_delete=models.CASCADE, primary_key=True, related_name="basket", verbose_name="Пользователь"
    )
    recipient = models.CharField("Получатель", max_length=255, blank=True, null=True)
    contact = models.CharField("Контакты", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.pk)

    @property
    def get_total_cost(self):
        """Для получения общей стоимости товаров в корзине."""
        prices = [product.get_total_price for product in self.ordered_n.all()]
        quantities = [product.quantity for product in self.ordered_n.all()]
        total_cost = sum([price * quantity for price, quantity in zip(prices, quantities, strict=False)])
        return int(total_cost)

    @property
    def get_total_quantity(self):
        """Для получения количества товаров в корзине."""
        products = sum([product.quantity for product in self.ordered_n.all()])
        return products

    @property
    def get_discount(self):
        """Для получения скидки на корзину."""
        if not hasattr(self, "_request"):
            return 0

        coupon_id = self._request.session.get("coupon_id")
        if not coupon_id:
            return 0

        try:
            coupon = Coupon.objects.get(id=coupon_id, is_active=True)
            if coupon.is_valid():
                result = self.get_total_cost * Decimal(coupon.discount) / 100
                return int(result)
        except Coupon.DoesNotExist:
            self._clear_coupon_session()
            return 0

    @property
    def get_total_with_discount(self):
        """Рассчитывает итоговую сумму только со скидкой."""
        total_cost = self.get_total_cost
        discount = self.get_discount

        if discount is None:
            discount = 0

        res = int(total_cost - discount)

        return res

    @property
    def get_total_with_discount_and_cashback(self):
        """Возвращает сумму с применением купона и скидки."""

        total = self.get_total_cost
        if self._request.session.get("coupon_id"):
            total = self.get_total_with_discount

        if self._request.session.get("use_cashback") and hasattr(self._request.user, "cashback_balance"):
            cashback = min(self._request.user.cashback_balance.total, total)
            return total - cashback
        return total

    def bind_request(self, request):
        """Привязывает request к корзине."""
        self._request = request
        return self

    def _clear_coupon_session(self):
        """Очищает данные купона из сессии"""
        if hasattr(self, "_request"):
            for key in ["coupon_id", "coupon_code", "coupon_discount"]:
                self._request.session.pop(key, None)


class BasketProduct(TimeStamp, models.Model):
    """Привязка продукта к корзине, артикул товара."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="ordered_n")
    quantity = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"

    def __str__(self):
        return self.product.title

    @property
    def get_total_price(self):
        """Для получения стоимости товаров в корзине."""
        return self.product.price * self.quantity
