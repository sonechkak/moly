FROM python:3.13-alpine

LABEL maintainer="Sonya Karmeeva"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY src /app

RUN mkdir -p /vol/web/media /vol/web/static && \
    adduser -D sonya && \
    chown -R sonya:sonya /vol/ && \
    chmod -R 755 /vol/web

USER sonya

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]