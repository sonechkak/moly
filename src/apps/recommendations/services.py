import logging

from apps.favs.models import FavoriteProducts
from apps.orders.models import OrderProduct
from apps.shop.models import Product
from django.db import transaction
from django.db.models import Count, F, Max, Q
from django.utils import timezone

from .models import Similarity, UserPageVisit

logger = logging.getLogger("user.actions")


class RecommendationService:
    """Класс для работы с рекомендациями."""

    @classmethod
    def _get_user_products(cls, user):
        """Получить все товары, с которыми взаимодействовал пользователь."""

        visited = UserPageVisit.objects.filter(user=user)
        favorites = FavoriteProducts.objects.filter(user=user).select_related("product")
        ordered = OrderProduct.objects.filter(order__customer=user.profile).select_related("product")

        products = {}

        # Товарам присвоим вес от 1 до 5 по visit_count
        for visit in visited:
            products[visit.product_id] = max(products.get(visit.product_id, 0), min(5, visit.visit_count))

        # Избранным товарам вес 6
        for fav in favorites:
            products[fav.product_id] = max(products.get(fav.product_id, 0), 6)

        # Товары из корзины вес 7
        for order_item in ordered:
            products[order_item.product_id] = max(products.get(order_item.product_id, 0), 7)

        return products

    @classmethod
    def _get_similar_products(cls, user_products, user, limit=10):
        """Получить все товары, похожие на товары пользователя."""

        if not user_products:
            logger.error(
                f"Пользователь {user} не взаимодействовал с товарами. Hе могу получить рекомендации.",
                extra={
                    "user": user.username,
                },
            )
            return []

        # Похожие товары
        try:
            similarities = Similarity.objects.filter(
                Q(product_1_id__in=user_products.keys()) | Q(product_2_id__in=user_products.keys())
            ).only("product_1_id", "product_2_id", "similarity_score")
        except Similarity.DoesNotExist:
            cls.update_similarity_scores()
            # Получаем все товары, которые похожи на товары пользователя
            similarities = Similarity.objects.filter(
                Q(product_1_id__in=user_products.keys()) | Q(product_2_id__in=user_products.keys())
            ).only("product_1_id", "product_2_id", "similarity_score")

        recommendations = {}

        for sim in similarities:
            if sim.product_1_id in user_products:
                source, recommended = sim.product_1_id, sim.product_2_id
            elif sim.product_2_id in user_products:
                source, recommended = sim.product_2_id, sim.product_1_id
            else:
                continue

            # Вес рекомендации
            weight = sim.similarity_score * user_products.get(source, 0)
            recommendations[recommended] = recommendations.get(recommended, 0) + weight

        logger.info(
            f"Пользователь {user} получил рекомендации.",
            extra={
                "user": user.username,
                "recommendations": recommendations,
            },
        )
        return sorted(recommendations, key=recommendations.get, reverse=True)[:limit]

    @classmethod
    def get_recommendations(cls, limit=10, user=None):
        """Получить рекомендации для пользователя."""

        if user is None or not user.is_authenticated:
            return cls.get_default_recommendations()

        user_products = cls._get_user_products(user)
        if not user_products:
            return cls.get_default_recommendations()

        # Получаем похожие товары
        similar_products = cls._get_similar_products(user_products=user_products, user=user)

        recommendations = Product.objects.filter(id__in=similar_products, available=True).distinct()[:limit]

        # Если рекомендаций мало, то добавляем популярные товары
        if len(recommendations) < limit:
            fallback = cls.get_recommendations(limit - len(recommendations))
            recommendations = list(recommendations) + list(fallback)

        return recommendations

    @classmethod
    def get_default_recommendations(cls, limit=10):
        """Рекомендации по умолчанию, если нет данных о пользователе."""

        if limit is None:
            limit = 10

        popular = Product.objects.filter(available=True).annotate(popularity=Count("watched")).order_by("-popularity")

        # Половина популярных и случайных
        half = limit // 2
        result = list(popular[:half])

        if len(result) < limit:
            random_products = (
                Product.objects.filter(available=True)
                .exclude(id__in=[p.pk for p in result])
                .order_by("watched")[: limit - half]
            )
            result.extend(random_products)

        return result

    @classmethod
    def calculate_similarity(cls, product_1, product_2, weights=None):
        """Вычислить similarity_score между двумя товарами."""

        if product_1 == product_2:
            raise ValueError("Нельзя сравнивать товар с самим собой.")

        default_weights = {
            "views": 0.4,
            "category": 0.2,
            "price": 0.2,
            "rating": 0.2,
            "orders": 0.2,
        }

        if weights is None:
            weights = default_weights
        else:
            total = sum(weights.values())
            weights = {k: v / total for k, v in weights.items()}

        # Категории
        category_score = 1 if product_1.category == product_2.category else 0

        # Цена
        max_price = Product.objects.aggregate(max_price=Max("price"))["max_price"]
        price_diff = abs(product_1.price - product_2.price)
        price_score = 1 - min(price_diff / max_price, 1)

        # Рейтинг
        rating_diff = abs(product_1.get_rating - product_2.get_rating)
        rating_score = 1 - min(rating_diff / 5, 1)  # Рейтинг от 0 до 5

        # Популярность
        views_diff = abs(product_1.watched - product_2.watched)
        max_views = Product.objects.aggregate(max_views=Max("watched"))["max_views"]
        views_score = 1 - min(views_diff / max_views, 1)

        # Товары в корзине
        common_orders = (
            OrderProduct.objects.filter(product__in=[product_1, product_2])
            .values("order_id")
            .annotate(cnt=Count("product_id"))
            .filter(cnt=2)
            .count()
        )

        max_common_orders = OrderProduct.objects.values("order_id").distinct().count() or 1
        orders_score = min(common_orders / max_common_orders * 2, 1)

        # Итоговый score
        total_score = (
            category_score * weights.get("category", 0)
            + price_score * weights.get("price", 0)
            + rating_score * weights.get("rating", 0)
            + views_score * weights.get("views", 0)
            + orders_score * weights.get("orders", 0)
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
    def update_similarity_scores(cls, batch_size=100):
        """Обновить таблицу Similarity с рассчитанными значениями."""

        product_ids = Product.objects.values_list("id", flat=True)
        total = len(product_ids)

        for i in range(0, total, batch_size):
            batch = product_ids[i : i + batch_size]
            products = Product.objects.in_bulk(batch)

            for p1_id, product_1 in products.items():
                for p2_id in product_ids[i + 1 :]:
                    if p1_id == p2_id:
                        continue

                    product_2 = products.get(p2_id)
                    if not product_2:
                        continue

                    similarity_score = cls.calculate_similarity(product_1, product_2)

                    Similarity.objects.update_or_create(
                        product_1_id=min(p1_id, p2_id),
                        product_2_id=max(p1_id, p2_id),
                        defaults={"similarity_score": similarity_score},
                    )
