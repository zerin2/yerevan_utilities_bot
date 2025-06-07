import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AsyncIO

from settings import settings

redis_broker = RedisBroker(url=settings.redis_url)
redis_broker.add_middleware(AsyncIO())
dramatiq.set_broker(redis_broker)


# TODO тут добавляем ссылку на функцию воркера
