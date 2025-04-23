import logging

from apps.favs.models import FavoriteProducts
from apps.shop.models import Product
from django.core.exceptions import FieldError
from django.db import transaction
from django.db.models import Count, F, Q
from django.utils import timezone

from .models import Similarity, UserPageVisit

logger = logging.getLogger("user.actions")


class RecommendationService:
    """Класс для работы с рекомендациями."""

    @classmethod
    def track_product_view(cls, user, product):
        """Отслеживание просмотра товара пользователем."""
        if not user or not user.is_authenticated:
            product.watched += 1
            product.save(update_fields=["watched"])
            return

        with transaction.atomic():
            # Пытаемся обновить существующую запись
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

    @classmethod
    def get_recommendations(cls, user=None, limit=10, exclude=None):
        """Получить рекомендации для пользователя."""
        if user is None or not user.is_authenticated:
            return cls._get_fallback_recommendations(limit)

        user_products = cls._get_user_products(user)
        if not user_products:
            return cls._get_fallback_recommendations(limit)

        # Получаем похожие товары
        similar_products = cls._get_similar_products(user_products, limit * 2)

        if exclude:
            similar_products = [p for p in similar_products if p != exclude.pk]

        recommendations = Product.objects.filter(id__in=similar_products, available=True).distinct()[:limit]

        # Если рекомендаций мало, то добавляем популярные товары
        if len(recommendations) < limit:
            fallback = cls._get_fallback_recommendations(limit - len(recommendations))
            recommendations = list(recommendations) + list(fallback)

        return recommendations

    @classmethod
    def _get_user_products(cls, user):
        """Получить все товары, с которыми взаимодействовал пользователь."""
        visited = list(UserPageVisit.objects.filter(user=user))
        favorites = list(FavoriteProducts.objects.filter(user=user))

        products = {}

        # Товарам присвоим вес от 1 до 5 по visit_count
        for visit in visited:
            products[visit.product_id] = min(5, visit.visit_count)

        # Избранным товарам даём вес 5
        for fav in favorites:
            products[fav.product_id] = 5

        return products

    @classmethod
    def _get_similar_products(cls, user_products, limit):
        """Получить все товары, похожие на товары пользователя."""

        similarities = Similarity.objects.filter(
            Q(product_1_id__in=user_products.keys()) | Q(product_2_id__in=user_products.keys())
        )

        # Собираем рекомендации с весами
        recommendations = {}

        for sim in similarities:
            if sim.product_1_id in user_products:
                source, recommended = sim.product_1_id, sim.product_2_id
            else:
                source, recommended = sim.product_2_id, sim.product_1_id

            # Рассчитываем вес рекомендации
            weight = sim.similarity_score * user_products[source]

            # Добавляем в рекомендации
            if recommended in recommendations:
                recommendations[recommended] += weight
            else:
                recommendations[recommended] = weight

        # Сортируем по весу и возвращаем топ
        return sorted(recommendations.keys(), key=lambda x: recommendations[x], reverse=True)[:limit]

    @classmethod
    def _get_fallback_recommendations(cls, limit):
        """Рекомендации по умолчанию, если нет данных о пользователе."""
        popular = (
            Product.objects.filter(available=True)
            .annotate(popularity=Count("watched"))
            .order_by("-popularity")[: limit * 2]
        )

        # Берём половину популярных и половину случайных
        half = limit // 2
        result = list(popular[:half])

        if len(result) < limit:
            random_products = Product.objects.filter(available=True).exclude(id__in=[p.id for p in result])[
                : limit - half
            ]
            result.extend(random_products)

        return result
