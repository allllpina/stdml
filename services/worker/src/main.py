import asyncio
import logging

from src.adapters.inbound.kafka_listener import KafkaInboundListener
from src.adapters.outbound.feast_provider import FeastFeatureProvider
from src.adapters.outbound.mlflow_provider import MLflowModelProvider
from src.adapters.outbound.redis_storage import RedisResultStorage
from src.config import settings
from src.domain.use_cases import InferenceService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for the ML Worker service."""
    logger.info("Initializing ML Worker service...")

    # --- 1. Outbound Adapters Initialization ---
    logger.info("Setting up outbound adapters...")
    feature_provider = FeastFeatureProvider(repo_path=settings.feast_repo_path)

    model_provider = MLflowModelProvider(tracking_uri=settings.mlflow_tracking_uri)
    # Pre-load the champion model before starting to consume messages
    logger.info(f"Pre-loading initial champion model: '{settings.initial_model_name}'")
    try:
        model_provider.load_model(settings.initial_model_name)
    except Exception as e:
        logger.error(f"Failed to load initial model: {e}")
        raise

    result_storage = RedisResultStorage(redis_url=settings.redis_url)

    # --- 2. Domain Use Cases Initialization ---
    logger.info("Setting up domain use cases...")
    inference_service = InferenceService(
        feature_provider=feature_provider,
        model_provider=model_provider,
        result_storage=result_storage,
    )

    # --- 3. Inbound Adapters Initialization ---
    logger.info("Setting up inbound adapters...")
    kafka_listener = KafkaInboundListener(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        inference_topic=settings.kafka_inference_topic,
        control_topic=settings.kafka_control_topic,
        group_id=settings.kafka_group_id,
        inference_service=inference_service,
    )

    # --- 4. Start Service ---
    logger.info("Starting ML Worker Kafka Listener...")
    await kafka_listener.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
    except Exception:
        logger.exception("Fatal error occurred in ML Worker.")
