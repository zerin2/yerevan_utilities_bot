from redis.asyncio import Redis
from redis.exceptions import (
    ConnectionError,
    RedisError,
    TimeoutError,
)

from logs.config import bot_logger
from settings import settings


def create_redis() -> Redis:
    try:
        return Redis(
            host=settings.get_redis_host,
            port=settings.redis_port,
            decode_responses=True,
        )
    except (ConnectionError, TimeoutError, RedisError) as e:
        bot_logger.error(f'Ошибка подключения к Redis: {str(e)}')
        return None


redis_client = create_redis()
