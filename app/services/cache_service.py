from app.core.redis import redis_client
from app.core.logger import get_logger
import json
from typing import Optional, Any

logger = get_logger("cache_service")

class CacheService:
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl

    async def get_cached_question(self, question_id: int) -> Optional[dict]:
        """Получить вопрос из кэша"""
        try:
            key = f"question:{question_id}"
            cached = await redis_client.get_key(key)
            if cached:
                logger.debug(f"Cache hit for question {question_id}")
                return json.loads(cached)
            logger.debug(f"Cache miss for question {question_id}")
            return None
        except Exception as e:
            logger.error(f"Error getting cached question {question_id}: {e}")
            return None

    async def set_cached_question(self, question_id: int, question_data: dict):
        """Сохранить вопрос в кэш"""
        try:
            key = f"question:{question_id}"
            await redis_client.set_key(
                key,
                json.dumps(question_data, default=str),
                self.default_ttl
            )
            logger.debug(f"Question {question_id} cached")
        except Exception as e:
            logger.error(f"Error setting cached question {question_id}: {e}")

    async def invalidate_question(self, question_id: int):
        """Удалить вопрос из кэша"""
        try:
            key = f"question:{question_id}"
            await redis_client.delete_key(key)
            logger.debug(f"Question {question_id} invalidated from cache")
        except Exception as e:
            logger.error(f"Error invalidating question {question_id}: {e}")

    async def get_cached_questions_list(self) -> Optional[list]:
        """Получить список вопросов из кэша"""
        try:
            key = "questions:list"
            cached = await redis_client.get_key(key)
            if cached:
                logger.debug("Cache hit for questions list")
                return json.loads(cached)
            logger.debug("Cache miss for questions list")
            return None
        except Exception as e:
            logger.error(f"Error getting cached questions list: {e}")
            return None

    async def set_cached_questions_list(self, questions_data: list):
        """Сохранить список вопросов в кэш"""
        try:
            key = "questions:list"
            await redis_client.set_key(
                key,
                json.dumps(questions_data, default=str),
                self.default_ttl
            )
            logger.debug("Questions list cached")
        except Exception as e:
            logger.error(f"Error setting cached questions list: {e}")

    async def invalidate_questions_list(self):
        """Удалить список вопросов из кэша"""
        try:
            key = "questions:list"
            await redis_client.delete_key(key)
            logger.debug("Questions list invalidated from cache")
        except Exception as e:
            logger.error(f"Error invalidating questions list: {e}")

# Глобальный экземпляр сервиса кэширования
cache_service = CacheService()