FROM python:3.13.3-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/* && \
    uv sync --no-dev --no-cache --locked && \
    uv run python -m unidic download

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py"]
