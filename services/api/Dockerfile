FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY services/api/pyproject.toml ./services/api/

RUN uv sync --no-dev --package api --no-install-project

COPY services/api/src ./src

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH="/app/src"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
