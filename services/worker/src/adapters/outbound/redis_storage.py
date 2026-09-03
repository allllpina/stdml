import logging
from typing import override

import redis

from src.domain.entities import PredictionResult
from src.ports.result_storage import ResultStorage

logger = logging.getLogger(__name__)


class RedisResultStorage(ResultStorage):
    """Implementation of ResultStorage using Redis (synchronous client)."""

    def __init__(self, redis_url: str):
        self._redis = redis.Redis.from_url(redis_url, decode_responses=True)

    @override
    def save(self, result: PredictionResult) -> None:
        key = f"result:{result.respondent_id}"

        payload = result.model_dump_json()

        try:
            self._redis.set(key, payload)
            logger.info(
                f"Result for respondent_id={result.respondent_id} successfully stored in Redis under the key {key}"
            )
        except Exception as e:
            logger.error(f"Error saving the result in Redis for respondent_id={result.respondent_id}: {e}")
            raise RuntimeError("Failed to save the result to Redis") from e
