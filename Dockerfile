#python:3.10.16-alpine3.21
FROM python:3.13-alpine as poetry

#Hadolint DL4006
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

#RUN adduser -h /app -D python &&      apk add --no-cache poetry
RUN adduser -h /app -D python

#USER python
WORKDIR /

ENV POETRY_HOME="/" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV PATH="/app/venv/bin:/app/.local/bin:${PATH}"

COPY ./pyproject.toml ./poetry.lock   /

RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

RUN poetry install --only main --no-root && \
     chown -R python:python /.venv

#python:3.10.16-alpine3.21
FROM python:3.13-alpine as runtime

RUN adduser -h /app -D python && \
     apk add --no-cache gettext
USER python

WORKDIR /app


# Копируем код проекта

COPY entrypoint.sh /app/entrypoint.sh

# Создаем и настраиваем пользователя
COPY --chown=python:python --from=poetry /.venv /.venv
ENV PATH="/.venv/bin:${PATH}"

COPY --chown=python:python ./src ./pyproject.toml ./poetry.lock /app/

CMD ["/app/entrypoint.sh"]
