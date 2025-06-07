import asyncio

from core.cache_settings import redis_client
from core.logger_settings import logger
from workers.async_rq_worker.init_worker import AsyncRQWorker
from workers.tasks import start_parsing

rq_worker2 = AsyncRQWorker(
    redis_client=redis_client,
    queue_names=['parsing_queue'],
    function=start_parsing,
    logger=logger,
)

if __name__ == '__main__':
    asyncio.run(rq_worker2.run())
