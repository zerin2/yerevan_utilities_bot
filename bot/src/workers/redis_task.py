import json
from dataclasses import dataclass
from typing import List, Optional, Tuple

from redis import Redis

import workers.config as conf


@dataclass
class RedisTask:
    _redis: Redis = conf.REDIS_CLIENT

    high_queue_parser: str = None
    low_queue_parser: str = None
    high_queue_bot: str = None
    low_queue_bot: str = None

    for_bot: List[str] = None
    for_parser: List[str] = None

    def __post_init__(self):
        self.high_queue_parser = conf.HIGH_REDIS_QUEUE_PARSER
        self.low_queue_parser = conf.LOW_REDIS_QUEUE_PARSER

        self.high_queue_bot = conf.HIGH_REDIS_QUEUE_BOT
        self.low_queue_bot = conf.LOW_REDIS_QUEUE_BOT

        self.for_bot = [self.high_queue_bot, self.low_queue_bot]
        self.for_parser = [self.high_queue_parser, self.low_queue_parser]

    def get_priority_task(self, sender: str) -> Optional[Tuple[bytes, bytes]]:
        queues = self.for_parser if sender == 'bot' else self.for_bot
        return self._redis.blpop(queues)

    def create_task(self, data: dict, priority: str, consumer: str) -> None:
        if consumer == 'bot':
            queue = self.high_queue_bot if priority == 'high' else self.low_queue_bot
        elif consumer == 'parser':
            queue = self.high_queue_parser if priority == 'high' else self.low_queue_parser
        else:
            raise ValueError('consumer должен быть \'bot\' или \'parser\'')
        self._redis.lpush(queue, json.dumps(data))
