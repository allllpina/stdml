from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.communicators.kafka_communicator import KafkaCommunicator
from src.communicators.mlflow_communicator import DagsHubCommunicator
from src.communicators.redis_communicator import RedisCommunicator
from src.core.config import settings
from src.routers.model_router import router as model_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage the application lifecycle (Startup / Shutdown)."""
    broker = KafkaCommunicator(bootstrap_servers=settings.kafka_bootstrap_servers)
    cache = RedisCommunicator(redis_url=settings.redis_url)
    mlflow = DagsHubCommunicator(tracking_uri=settings.mlflow_tracking_uri)

    await broker.start()

    app.state.broker = broker
    app.state.cache = cache
    app.state.mlflow = mlflow

    yield

    await broker.close()


def create_app() -> FastAPI:
    """Application factory for convenient testing and initialization."""
    app = FastAPI(
        title=settings.project_name,
        description="Головний шлюз для інференсу моделей та взаємодії з Kafka",
        version=settings.version,
        lifespan=lifespan,
    )

    app.include_router(router=model_router, prefix="/api/v1")

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
