# E-commerce Project

Проект интернет-магазина на Django с системой оплаты Stripe.

## Технологии

- Python 3.13
- Django
- Celery
- Redis
- PostgreSQL
- Poetry

## Основные функции

- Каталог товаров с категориями
- Система подписок на товары и категории
- Автоматические уведомления об изменениях
- Корзина покупок
- Список избранного
- Система заказов
- Система оплаты заказов

## Установка и запуск

### Локальная разработка

1. Клонировать репозиторий:
```bash
git clone git@github.com:sonechkak/moly.git
```

2. Установить зависимости:
```bash
poetry install
```

3. Создать и настроить .env файл:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=user
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

4. Применить миграции:
```bash
poetry run python manage.py migrate
```

5. Запустить сервер:
```bash
poetry run python manage.py runserver
```

### Docker

1. Собрать образ:
```bash
docker build -t ecommerce .
```

2. Запустить контейнер:
```bash
docker run -p 8000:8000 --env-file .env ecommerce
```

## Celery задачи

1. Запустить Redis:
```bash
redis-server
```

2. Запустить Celery worker:
```bash
cd src
celery --app conf worker -l debug
```

3. Запустить Celery beat:
```bash
celery -A conf beat -l info
```

## Тестирование

Запуск тестов:
```bash
poetry run python manage.py test
```

## Автор

Sonya Karmeeva

## Лицензия

MIT