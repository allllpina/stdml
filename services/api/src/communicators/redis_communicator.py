import json
from typing import Any, cast

import redis.asyncio as redis

from .base import CacheCommunicator


class RedisCommunicator(CacheCommunicator):
    def __init__(self, redis_url: str):
        """
        Initializes the Redis connection pool.
        Using redis.asyncio.Redis explicitly helps Mypy resolve the client type.
        """
        self._redis = redis.Redis.from_url(redis_url, decode_responses=True)

    async def get_model(self) -> str | None:
        """Retrieves the currently active model name."""
        raw_model = await self._redis.get("current_model")
        return cast(str | None, raw_model)

    async def get_results(self, respondent_id: int) -> dict[str, Any] | None:
        """Retrieves the inference results for a specific respondent."""
        key = f"result:{respondent_id}"
        raw_result = await self._redis.get(key)

        if raw_result is None:
            return None

        str_result = cast(str, raw_result)

        try:
            parsed_data = json.loads(str_result)
            return cast(dict[str, Any], parsed_data)
        except json.JSONDecodeError:
            return None

    async def close(self) -> None:
        """Closes the Redis connection pool gracefully on app shutdown."""
        await self._redis.aclose()
