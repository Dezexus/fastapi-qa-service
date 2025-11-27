import redis.asyncio as redis
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("redis")

class RedisClient:
    def __init__(self):
        self.redis_client = None

    async def init_redis(self):
        """Инициализация подключения к Redis"""
        try:
            self.redis_client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def close_redis(self):
        """Закрытие подключения к Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")

    async def set_key(self, key: str, value: str, expire: int = 3600):
        """Установка ключа с временем жизни"""
        try:
            await self.redis_client.setex(key, expire, value)
        except Exception as e:
            logger.error(f"Error setting Redis key {key}: {e}")

    async def get_key(self, key: str) -> str:
        """Получение значения по ключу"""
        try:
            return await self.redis_client.get(key)
        except Exception as e:
            logger.error(f"Error getting Redis key {key}: {e}")
            return None

    async def delete_key(self, key: str):
        """Удаление ключа"""
        try:
            await self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting Redis key {key}: {e}")

    async def keys(self, pattern: str = "*"):
        """Получение ключей по паттерну"""
        try:
            return await self.redis_client.keys(pattern)
        except Exception as e:
            logger.error(f"Error getting Redis keys with pattern {pattern}: {e}")
            return []

# Глобальный экземпляр Redis клиента
redis_client = RedisClient()