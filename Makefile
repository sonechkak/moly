.PHONY: help install dev test prod migrate migrations shell lint clean docker-dev docker-test docker-prod

# Переменные
PYTHON = python
MANAGE = src/manage.py
SETTINGS_DEV = settings.dev
SETTINGS_TEST = settings.test
SETTINGS_PROD = settings.prod

# Цвета для вывода
GREEN = \033[0;32m
NC = \033[0m # No Color
INFO = @printf "${GREEN}%s${NC}\n"

help:
	@echo "Доступные команды:"
	@echo "make install    - Установка зависимостей через poetry"
	@echo "make dev        - Запуск сервера для разработки"
	@echo "make test       - Запуск тестов"
	@echo "make prod       - Запуск production сервера"
	@echo "make migrate    - Применить миграции"
	@echo "make migrations - Создать миграции"
	@echo "make shell      - Запуск Django shell"
	@echo "make lint       - Проверка кода (flake8, black)"
	@echo "make clean      - Очистка кэша и временных файлов"
	@echo "make docker-dev - Запуск dev окружения в Docker"
	@echo "make docker-test- Запуск тестов в Docker"
	@echo "make docker-prod- Запуск prod окружения в Docker"

install:
	$(INFO) "Установка зависимостей..."
	poetry install

infra:
	docker compose up -d db
	docker compose up -d redis
	docker compose up -d mailpit

dev:
	export DJANGO_SETTINGS_MODULE=settings.dev
	python src/manage.py migrate
	python src/manage.py runserver 0.0.0.0:8000
	celery -A src.conf beat --loglevel=info --settings=settings.dev
	celery -A src.conf worker --loglevel=info --settings=settings.dev

dev-stop:
	$(INFO) "Остановка всех процессов..."
	pkill -f "celery worker" || true
	pkill -f "celery beat" || true
	pkill -f "runserver" || true

test:
	$(INFO) "Запуск тестов..."
	export DJANGO_SETTINGS_MODULE=settings.test
	python src/manage.py test src/apps/shop/tests

#prod:
#	$(INFO) "Запуск production сервера..."
#	docker compose up -d db
#	docker compose up -d redis
#	docker compose up -d mailpit
#	export DJANGO_SETTINGS_MODULE=settings.prod
#	python src/manage.py runserver 0.0.0.0:8000

migrations:
	$(INFO) "Создаем миграции..."
	python src/manage.py makemigrations

migrate:
	$(INFO) "Создаем миграции..."
	python src/manage.py migrate

shell:
	$(INFO) "Запуск Django shell..."
	export DJANGO_SETTINGS_MODULE=settings.dev
	python src/manage.py shell

lint:
	$(INFO) "Проверка кода..."
	flake8 src/
	black src/ --check

#clean:
#	$(INFO) "Очистка кэша и временных файлов..."
#	find . -type d -name "__pycache__" -exec rm -r {} +
#	find . -type f -name "*.pyc" -delete
#	find . -type f -name "*.pyo" -delete
#	find . -type f -name "*.pyd" -delete
#	find . -type f -name ".coverage" -delete
#	find . -type d -name "*.egg-info" -exec rm -r {} +
#	find . -type d -name "*.egg" -exec rm -r {} +
#	find . -type d -name ".pytest_cache" -exec rm -r {} +
#	find . -type d -name ".coverage" -exec rm -r {} +

# Docker команды
docker-dev:
	$(INFO) "Запуск dev окружения в Docker..."
	docker compose -f docker-compose.yml up -d --build web
	docker compose -f docker-compose.yml up -d --build celery
	docker compose -f docker-compose.yml up -d --build celery-beat

docker-test:
	$(INFO) "Запуск тестов в Docker..."
	docker compose -f docker-compose.yml up -d --build web
	docker compose -f docker-compose.yml up -d --build celery
	 compose -f docker-compose.yml up -d --build celery-beatdocker

docker-prod:
	$(INFO) "Запуск prod окружения в Docker..."
	docker compose -f docker-compose.yml up -d --build web
	docker compose -f docker-compose.yml up -d --build celery
	docker compose -f docker-compose.yml up -d --build celery-beat

# Команды для работы с зависимостями
deps-update:
	$(INFO) "Обновление зависимостей..."
	poetry update

deps-lock:
	$(INFO) "Блокировка версий зависимостей..."
	poetry lock

## Команды для работы со статическими файлами
#collectstatic:
#	$(INFO) "Сбор статических файлов..."
#	DJANGO_SETTINGS_MODULE=$(SETTINGS_PROD) $(PYTHON) $(MANAGE) collectstatic --noinput

# Команды для создания суперпользователя
createsuperuser:
	$(INFO) "Создание суперпользователя..."
	DJANGO_SETTINGS_MODULE=$(SETTINGS_DEV) $(PYTHON) $(MANAGE) createsuperuser
