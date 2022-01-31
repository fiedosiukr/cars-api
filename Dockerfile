FROM python:3.10.1-slim-buster

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install build-essential libseccomp-dev libpq-dev libpcre3-dev postgresql-client -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry \
    && rm -rf /root/.cache/pip

WORKDIR /code
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root \
    && rm -rf /root/.cache/pypoetry /root/.cache/pip

COPY . .
RUN chmod +x /code/docker/wait-for-it.sh /code/docker/dev-entrypoint.sh
