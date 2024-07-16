# syntax = docker/dockerfile:1.3

FROM docker.io/debian:bookworm-slim as base

ARG APP_HOME=/home/app/parat

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        netcat-openbsd \
        # For translations
        gettext \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --uid 1000 --disabled-password --gecos '' --home /app app \
    && install -d -o app -g app /home/app/parat /venv

WORKDIR /home/app/parat/
ENTRYPOINT ["./docker/django/entrypoint"]


FROM base as builder
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=app:app ./requirements .
USER app
RUN --mount=type=cache,target=/home/app/.cache,uid=1000 \
    python3 -m venv /venv \
    && /venv/bin/pip3 install -r production.txt
EXPOSE 8000


FROM base as dev
COPY --from=builder /venv /venv
COPY --chown=app:app . ${APP_HOME}
USER app
RUN --mount=type=cache,target=/home/app/.cache,uid=1000 \
    /venv/bin/pip3 install -r requirements/development.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as app
COPY --from=builder /venv /venv
COPY --chown=app:app . ${APP_HOME}
USER app
RUN DJANGO_DATABASE_URL="postgres://user@host/db" python manage.py collectstatic \
	&& DJANGO_DATABASE_URL="postgres://user@host/db" python manage.py compilemessages \
	&& rm -rf ui/
CMD ["gunicorn", "config.wsgi:application", "--bind", "[::]:8000", "--user", "app", "--workers", "3", "--log-level", "debug"]
