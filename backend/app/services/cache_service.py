from typing import Optional, Any
import json
import hashlib
from redis import asyncio as aioredis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)

    def _generate_key(self, prefix: str, data: str) -> str:
        """Generate a unique cache key."""
        hash_obj = hashlib.md5(data.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"

    def get_animation_key(self, description: str) -> str:
        """Generate a unique key for animation caching."""
        return self._generate_key("animation", description)

    async def get(self, key: str) -> Optional[dict]:
        """Get value from cache with logging."""
        try:
            value = await self.redis.get(key)
            if value:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(value)
            logger.info(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None

    async def set(self, key: str, value: dict, expire: int = None):
        """Set value in cache with TTL."""
        try:
            ttl = expire or settings.CACHE_TTL
            await self.redis.set(
                key,
                json.dumps(value),
                ex=ttl
            )
            logger.info(f"Cached value for key: {key}, TTL: {ttl}s")
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")

    async def delete(self, key: str):
        """Delete value from cache."""
        try:
            await self.redis.delete(key)
            logger.info(f"Deleted cache key: {key}")
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")

    async def get_or_set(self, key: str, getter_func, expire: int = None) -> Any:
        """Get from cache or compute and cache value."""
        try:
            # Try to get from cache
            cached_value = await self.get(key)
            if cached_value is not None:
                return cached_value

            # Compute value
            value = await getter_func()
            
            # Cache the computed value
            await self.set(key, value, expire)
            
            return value
        except Exception as e:
            logger.error(f"Cache get_or_set error: {str(e)}")
            # Fall back to computing value without caching
            return await getter_func()