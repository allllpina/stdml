FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY services/worker/pyproject.toml ./services/worker/

RUN uv sync --no-dev --package worker --no-install-project

COPY services/worker/src ./src

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "src.main"]
