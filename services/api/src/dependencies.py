from functools import lru_cache

from src.core.config import Settings, settings


@lru_cache
def get_settings() -> Settings:
    """
    Dependency for injecting application settings.
    Uses lru_cache to ensure settings are instantiated only once.
    """
    return settings
