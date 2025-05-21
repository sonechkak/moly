import logging
from decimal import Decimal

from apps.cashback.enums.cashback_choices import CashbackChoices
from apps.cashback.models import Cashback
from apps.loyalty.models import LoyaltyLevel, UserLoyalty
from apps.notifications.services.create_notification import create_notification
from django.db import transaction

logger = logging.getLogger("user.actions")


class LoyaltyService:
    """Класс для работы с программой лояльности."""

    @staticmethod
    def get_or_create_user_loyalty(user):
        """Получить или создать уровень лояльности пользователя."""
        cashback_balance, created = Cashback.objects.get_or_create(user=user)
        user_loyalty, created = UserLoyalty.objects.get_or_create(
            user=user,
            defaults={
                "cashback": cashback_balance,
            },
        )

        if created or not user_loyalty.current_level:
            # Находим самый низкий уровень лояльности
            base_level = LoyaltyLevel.objects.order_by("min_points").first()

            if base_level:
                user_loyalty.current_level = base_level
                user_loyalty.save(update_fields=["current_level"])
            else:
                logger.error(
                    "Не найдены уровни лояльности в базе данных. Создайте хотя бы один уровень лояльности.",
                    extra={"user": user.username},
                )

        user_loyalty.update_level()

        return user_loyalty

    @staticmethod
    def calculate_cashback(order_amount, loyalty_level):
        """Рассчитывает кэшбэк на основе суммы заказа и уровня лояльности."""

        if not loyalty_level:
            logger.warning("Не указан уровень лояльности для расчета кэшбэка")
            return Decimal("0.00")

        cashback_percentage = loyalty_level.cashback_percentage
        cashback_amount = (Decimal(order_amount) * Decimal(cashback_percentage)) / Decimal("100")
        return cashback_amount

    @staticmethod
    def process_order_cashback(order):
        """Обрабатывает кэшбэк после сохранения заказа."""
        user = order.user

        if not user or not order.is_paid:
            return None

        with transaction.atomic():
            try:
                # Получаем или создаем объект лояльности пользователя
                loyalty = LoyaltyService.get_or_create_user_loyalty(user)

                # Увеличиваем общую сумму покупок
                loyalty.total_spent += order.total_amount
                loyalty.save(update_fields=["total_spent"])

                # Обновляем уровень лояльности
                loyalty.update_level()

                # Проверяем наличие уровня лояльности
                if not loyalty.current_level:
                    logger.error(
                        "Отсутствует уровень лояльности для пользователя после обновления",
                        extra={"user": user.username, "order_id": order.id},
                    )
                    return None

                # Рассчитываем кешбэк
                cashback_amount = LoyaltyService.calculate_cashback(
                    order_amount=order.total_amount, loyalty_level=loyalty.current_level
                )

                if cashback_amount > Decimal("0"):
                    # Начисление кэшбэка
                    cashback = Cashback.objects.create(
                        user=user, order=order, amount=cashback_amount, cashback_status=CashbackChoices.APPROVED
                    )

                    # Обновляем баланс кэшбэка
                    cashback_balance = loyalty.cashback
                    cashback_balance.total += cashback_amount
                    cashback_balance.total_cashback_earned += cashback_amount
                    cashback_balance.save()

                    create_notification(
                        user=user,
                        title="Кешбэк начислен!",
                        message=f"Вам начислен кешбэк {cashback_amount} ₽ за заказ №{order.id}.",
                        notification_type="cashback_earned",
                        url="/profile/loyalty/",
                    )

                    return cashback

            except Exception as e:
                logger.error(
                    f"Ошибка при обработке кэшбэка: {e!s}", extra={"user": user.username, "order_id": order.id}
                )

            return None
