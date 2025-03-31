FROM python:3.13-alpine

LABEL maintainer="Sonya Karmeeva"

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH=/app/src

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
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    chmod a+x /opt/poetry/bin/poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Копируем код проекта
COPY src/ /app/src/

# Создаем и настраиваем пользователя
RUN mkdir -p /vol/web/media /vol/web/static && \
    adduser -D user && \
    chown -R user:user /vol/ /app && \
    chmod -R 755 /vol/web

USER user

# Изменяем команду запуска
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]