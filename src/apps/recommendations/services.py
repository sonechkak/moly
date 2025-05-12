import logging
from collections import defaultdict

from apps.favs.models import FavoriteProducts
from apps.orders.models import OrderProduct
from apps.shop.models import Product
from django.db import transaction
from django.db.models import Count, F, Max, Q
from django.utils import timezone

from .models import Similarity, UserPageVisit

logger = logging.getLogger("user.actions")

MAX_VIEW_WEIGHT = 5
FAVORITE_WEIGHT = 6
ORDERED_WEIGHT = 7
DEFAULT_WEIGHTS = {"category": 0.2, "price": 0.2, "rating": 0.2, "views": 0.2, "orders": 0.2}


class RecommendationService:
    """Класс для работы с рекомендациями."""

    @classmethod
    def _get_user_products(cls, user):
        """Получить все товары, с которыми взаимодействовал пользователь."""

        visited = dict(UserPageVisit.objects.filter(user=user).values_list("product_id", "visit_count"))
        favorites = set(FavoriteProducts.objects.filter(user=user).values_list("product_id", flat=True))
        ordered = set(OrderProduct.objects.filter(order__customer=user.profile).values_list("product_id", flat=True))

        products = {}

        # Просмотренным товарам присвоим вес по visit_count
        for product_id, visit_count in visited.items():
            products[product_id] = min(visit_count, MAX_VIEW_WEIGHT)

        # Избранным товарам присвоим вес
        for product_id in favorites:
            current_weight = products.get(product_id, 0)  # Получаем текущий вес
            products[product_id] = max(current_weight, FAVORITE_WEIGHT)

        # Товарам из корзины присвоим вес
        for product_id in ordered:
            current_weight = products.get(product_id, 0)
            products[product_id] = max(current_weight, ORDERED_WEIGHT)

        return products

    @classmethod
    def _get_similar_products_for_product(cls, product, limit=10):
        """Получить все товары, похожие на указанный товар."""
        if not product or not isinstance(product, Product):
            return []

        # Получаем все записи Similarity, где значится товар
        similarities = Similarity.objects.filter(
            Q(product_1_id=product.id) | Q(product_2_id=product.id)
        ).select_related("product_1", "product_2")[: limit * 2]  # Берем с запасом

        similar_products = []

        for sim in similarities:
            if sim.product_1_id == product.id:
                similar_product = sim.product_2
            else:
                similar_product = sim.product_1

            # Проверяем, что товар доступен и не дублируется
            if similar_product.available and similar_product not in similar_products:
                similar_products.append(similar_product)

            if len(similar_products) >= limit:
                break

        return similar_products[:limit]

    @classmethod
    def _get_similar_products(cls, user_products, user, limit=10):
        """Получить все товары, похожие на товары пользователя."""

        if not user_products:
            logger.error(f"Пользователь {user} не имеет истории покупок.")
            return []

        # Инициализируем словарь с автоматическими нулями
        recommendations = defaultdict(float)

        # Похожие товары
        # cls._update_similarity_scores(500)
        similarities = Similarity.objects.filter(
            Q(product_1_id__in=user_products.keys()) | Q(product_2_id__in=user_products.keys())
        ).only("product_1_id", "product_2_id", "similarity_score")

        # Для пары похожих товаров определим товар, который уже принадлежит пользователю, и похожий
        for sim in similarities:
            if sim.product_1_id in user_products:
                source, recommended = sim.product_1_id, sim.product_2_id
            elif sim.product_2_id in user_products:
                source, recommended = sim.product_2_id, sim.product_1_id
            else:
                continue
            # Вес рекомендации = степень схожести (similarity_score) × вес товара для пользователя (weight)
            weight = sim.similarity_score * user_products[source]
            recommendations[recommended] += weight

        sorted_similarities = sorted(
            recommendations.keys(),
            key=lambda x: recommendations[x],  # по весу
            reverse=True,  # по убыванию
        )[:limit]

        logger.info(
            f"Пользователь {user} получил рекомендации.",
            extra={
                "user": user.username,
                "recommendations": recommendations,
            },
        )

        return sorted_similarities

    @classmethod
    def get_recommendations(cls, user, limit=10):
        """Получить рекомендации для пользователя."""

        if user is None or not user.is_authenticated:
            return cls._get_default_recommendations()
        else:
            user_products = cls._get_user_products(user)

        # Получаем похожие товары
        similar_products = cls._get_similar_products(user_products=user_products, user=user, limit=limit)

        # Формируем list рекомендаций из списка похожих товаров
        recommendations = list(Product.objects.filter(id__in=similar_products, available=True).distinct()[:limit])

        # Если рекомендаций мало, то добавляем дефолт товары
        if len(recommendations) < limit:
            fallback = limit - len(recommendations)
            recommendations.extend(cls._get_default_recommendations(limit=fallback))

        return recommendations

    @classmethod
    def _get_default_recommendations(cls, limit=10):
        """Рекомендации по умолчанию, если нет данных о пользователе."""

        if not isinstance(limit, int) or limit < 1:
            limit = 10

        # Получаем ids популярных товаров
        popular_products = list(
            Product.objects.filter(available=True).annotate(popularity=Count("watched")).order_by("-popularity")[:limit]
        )

        result = []

        result.extend(popular_products[:limit])

        return result[:limit]

    @classmethod
    def _calculate_similarity(cls, product_1, product_2, weights=None):
        """Вычислить similarity_score между двумя товарами."""

        if product_1.pk == product_2.pk:
            return 1.0

        # Нормализация весов
        weights = weights or DEFAULT_WEIGHTS
        if weights != DEFAULT_WEIGHTS:
            total = sum(weights.values())
            weights = {k: v / total for k, v in weights.items()}

        # Запросы к БД
        max_price = Product.objects.aggregate(max_price=Max("price"))["max_price"]
        max_views = Product.objects.aggregate(max_views=Max("watched"))["max_views"]
        common_orders = (
            OrderProduct.objects.filter(product__in=[product_1, product_2])
            .values("order_id")
            .annotate(cnt=Count("product_id"))
            .filter(cnt=2)
            .count()
        )
        total_orders = OrderProduct.objects.values_list("order_id").distinct().count() or 1

        # Категории
        category_score = int(product_1.category == product_2.category)

        # Цена
        price_diff = abs(product_1.price - product_2.price)
        price_score = 1 - min(price_diff / max_price, 1)

        # Рейтинг
        rating_diff = abs((product_1.get_rating or 0) - (product_2.get_rating or 0))
        rating_score = 1 - min(rating_diff / 5, 1)  # Рейтинг от 0 до 5

        # Просмотры
        views_diff = abs((product_1.watched or 0) - (product_2.watched or 0))
        views_score = 1 - min(views_diff / max_views, 1)

        # Товары в корзине
        orders_score = min(common_orders / total_orders * 2, 1)

        # Итоговый score
        total_score = sum(
            component * weights.get(key, 0)
            for key, component in [
                ("category", category_score),
                ("price", price_score),
                ("rating", rating_score),
                ("views", views_score),
                ("orders", orders_score),
            ]
        )

        return round(total_score, 4)

    @classmethod
    def track_product_view(cls, product, user=None):
        """Отслеживание просмотра товара пользователем."""

        if user is None or not user.is_authenticated:
            product.watched += 1
            product.save(update_fields=["watched"])
            logger.info(f"Анонимный пользователь открыл товар {product}.")

        with transaction.atomic():
            # Обновляем дату последнего просмотра
            updated = UserPageVisit.objects.filter(user=user, product=product).update(
                visit_count=F("visit_count") + 1, last_visited=timezone.now()
            )

            if not updated:
                UserPageVisit.objects.create(
                    user=user,
                    product=product,
                    visit_count=1,
                    first_visited=timezone.now(),
                    last_visited=timezone.now(),
                )

            logger.info(
                f"Пользователь {user} открыл товар {product.title}.",
                extra={
                    "product": product.title,
                    "user": user.username,
                },
            )

    @classmethod
    def _update_similarity_scores(cls, batch_size=100):
        """Обновление таблицы Similarity с рассчитанными значениями."""

        all_product_ids = Product.objects.values_list("id", flat=True)

        # Проходим по всем товарам по очереди
        for i, product_1_id in enumerate(all_product_ids):
            # Получаем первый товар
            product_1 = Product.objects.get(id=product_1_id)

            # Сравниваем только с последующими товарами без повторений
            for product_2_id in all_product_ids[i + 1 :]:
                # Получаем второй товар
                product_2 = Product.objects.get(id=product_2_id)

                # Вычисляем степень похожести (от 0 до 1)
                similarity = cls._calculate_similarity(product_1, product_2)

                # Сохраняем результат, упорядочивая ids без дублей
                Similarity.objects.update_or_create(
                    product_1_id=min(product_1_id, product_2_id),
                    product_2_id=max(product_1_id, product_2_id),
                    defaults={"similarity_score": similarity},
                )
