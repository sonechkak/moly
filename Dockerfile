FROM python:3.13-alpine

LABEL maintainer="Sonya Karmeeva"

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH=/app

WORKDIR /app

RUN apk update && apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    chmod a+x /opt/poetry/bin/poetry

# Файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Копируем код проекта
COPY src/ /app/src
COPY entrypoint.sh /app/entrypoint.sh

# Создаем и настраиваем пользователя
RUN mkdir -p /vol/web/media /vol/web/static /app/conf/beat && \
    adduser -D user && \
    chown -R user:user /vol/ /app && \
    chmod -R 755 /vol/web && \
    chmod -R 777 /app/conf/beat

USER user

CMD ["/app/entrypoint.sh"]
