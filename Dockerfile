FROM python:3.13-alpine

LABEL maintainer="Sonya Karmeeva"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apk add --update --no-cache postgresql-client jpeg-dev gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY src /app

RUN mkdir -p /vol/web/media /vol/web/static && \
    adduser -D sonya && \
    chown -R sonya:sonya /vol/ && \
    chmod -R 755 /vol/web

USER sonya