from fastapi import FastAPI
from src.core.config import settings


def create_app() -> FastAPI:
    """Фабрика створення застосунку для зручного тестування та ініціалізації."""

    app = FastAPI(
        title=settings.project_name,
        description="Головний шлюз для інференсу моделей та взаємодії з Kafka",
        version=settings.version,
    )

    # Base healthcheck
    @app.get("/health", tags=["System"])
    async def health_check() -> dict[str, str]:
        return {
            "service": settings.project_name,
            "version": settings.version,
            "status": "ok",
            "kafka_broker": settings.kafka_bootstrap_servers
        }

    return app

app = create_app()
