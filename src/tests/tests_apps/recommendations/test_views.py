import pytest
from django.utils import timezone

from apps.recommendations.models import Similarity, UserPageVisit
from apps.recommendations.services import RecommendationService
from apps.orders.models import Order, OrderProduct
from apps.favs.models import FavoriteProducts
from apps.users.models import Profile


@pytest.mark.django_db
def test_get_user_products(transactional_db, user, products):
        """Тест сбора информации о взаимодействиях пользователя с товарами"""
        # Создаем просмотры
        for i, product in enumerate(products[:3]):
            UserPageVisit.objects.create(
                user=user,
                product=product,
                visit_count=i + 1,
                last_visited=timezone.now()
            )

        # Добавляем в избранное
        FavoriteProducts.objects.create(user=user, product=products[2])

        # Создаем заказ с товарами
        order = Order.objects.create(customer=user.profile, is_complete=True)
        OrderProduct.objects.create(order=order, product=products[3], quantity=1, price=100)
        OrderProduct.objects.create(order=order, product=products[4], quantity=2, price=200)

        user_products = RecommendationService._get_user_products(user)

        assert len(user_products) == 5  # 3 просмотренных (один из них в избранном) + 2 в заказе
        assert user_products[products[2].id] == 6  # Избранный товар
        assert user_products[products[3].id] == 7  # Купленный товар
        assert user_products[products[0].id] == 1  # Просмотренный 1 раз


@pytest.mark.django_db
def test_similarity_calculation(transactional_db, user, products, categories):
    """Тест расчета схожести товаров с разными параметрами"""
    product1 = products[0]
    product2 = products[1]

    # Устанавливаем одинаковую категорию
    product1.category.add(categories[0])
    product2.category.add(categories[1])

    # Устанавливаем рейтинги
    product1.rating = 4.5
    product2.rating = 4.0

    # Создаем общие заказы
    order = Order.objects.create(customer=user.profile, is_complete=True)
    OrderProduct.objects.create(order=order, product=product1, quantity=1, price=100)
    OrderProduct.objects.create(order=order, product=product2, quantity=1, price=100)

    score = RecommendationService._calculate_similarity(product1, product2)

    assert (0.5 < score <= 1.0)  # Ожидаем высокий score из-за совпадений


@pytest.mark.django_db
def test_recommendations_priority(transactional_db, user, products):
        """Тест приоритетов рекомендаций (купленные > избранные > просмотренные)"""

        # Товар в корзине
        order = Order.objects.create(customer=user.profile, is_complete=True)
        OrderProduct.objects.create(order=order, product=products[0], quantity=1, price=100)

        # Избранный товар
        FavoriteProducts.objects.create(user=user, product=products[1])

        # Просмотренный товар
        UserPageVisit.objects.create(
            user=user,
            product=products[2],
            visit_count=3,
            last_visited=timezone.now()
        )

        RecommendationService._update_similarity_scores()

        recommendations = RecommendationService.get_recommendations(user=user, limit=20)
        rec_ids = [p.id for p in recommendations]

        # Похожие товары для каждого типа
        similar_to_ordered = Similarity.objects.filter(
            product_1=products[0]
        ).order_by('-similarity_score').first()

        similar_to_favorite = Similarity.objects.filter(
            product_1=products[1]
        ).order_by('-similarity_score').first()

        similar_to_viewed = Similarity.objects.filter(
            product_1=products[2]
        ).order_by('-similarity_score').first()

        assert similar_to_ordered.product_2_id in rec_ids
        assert similar_to_favorite.product_2_id in rec_ids
        assert similar_to_viewed.product_2_id in rec_ids
        assert rec_ids.index(similar_to_ordered.product_2_id) > rec_ids.index(similar_to_favorite.product_2_id)
        assert rec_ids.index(similar_to_favorite.product_2_id) > rec_ids.index(similar_to_viewed.product_2_id)


@pytest.mark.django_db
def test_track_product_view(transactional_db, user, products):
        """Тест трекинга просмотров товаров."""
        initial_count = products[0].watched

        RecommendationService.track_product_view(products[1], user)
        visit = UserPageVisit.objects.get(user=user, product=products[1])
        assert visit.visit_count == 1

        # Повторный просмотр
        RecommendationService.track_product_view(products[1], user)
        visit.refresh_from_db()
        assert visit.visit_count == 2


@pytest.mark.django_db
def test_default_recommendations(transactional_db, user, products):
        """Тест рекомендаций по умолчанию (для неавторизованных)"""
        # Увеличиваем популярность некоторых товаров
        products[0].watched = 100
        products[0].save()

        # Создаем заказы для товаров
        profile = Profile.objects.get(user=user)
        order = Order.objects.create(customer=profile, is_complete=True)
        OrderProduct.objects.create(order=order, product=products[1], quantity=5, price=100)

        recommendations = RecommendationService._get_default_recommendations(limit=4)

        assert len(recommendations) == 4


@pytest.mark.django_db
def test_empty_user_products(transactional_db, user):
        """Тест с пользователем без взаимодействий с товарами"""
        recommendations = RecommendationService.get_recommendations(user=user)
        assert recommendations == RecommendationService._get_default_recommendations()


@pytest.mark.django_db
def test_zero_price_in_similarity(transactional_db, products):
        """Тест с нулевой ценой при расчете схожести"""
        products[0].price = 0
        products[0].save()

        score = RecommendationService._calculate_similarity(products[0], products[1])
        assert 0 <= score <= 1


@pytest.mark.django_db
def test_identical_products(transactional_db, products):
        """Тест с одинаковыми товарами"""
        result = RecommendationService._calculate_similarity(products[0], products[0])
        assert result == 1.0
