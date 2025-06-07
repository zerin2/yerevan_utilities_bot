import asyncio
import json
import logging
import uuid
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Any, Awaitable, Callable, Optional

from pydantic import BaseModel, ValidationError
from redis.asyncio import Redis

from workers.async_rq_worker.enums import QueueStatus, WorkerMessage, FieldLength


class QueueValidator(BaseModel):
    queue_names: list[str]


@dataclass
class AsyncRQWorker:
    redis_client: Redis
    queue_names: list[str]
    task_id: str = None
    function: Optional[Callable[[dict], Awaitable[None]]] = None
    logger: Optional[logging.Logger] = None

    def __post_init__(self):
        self.queue_names = self.init_queues()
        self.logger = self.init_logger()
        self.function_name = (
            self.function.__name__
            if self.function is not None else None
        )

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def init_queues(self) -> list[str]:
        try:
            input_data = QueueValidator(queue_names=self.queue_names)
            return [
                name + QueueStatus.PROCESSING.value
                for name in input_data.queue_names
            ]
        except ValidationError as e:
            raise ValueError(
                WorkerMessage.QUEUE_VALIDATION_ERROR.value.format(error=e),
            )

    def init_logger(self) -> logging.Logger | Any:
        if self.logger is None:
            return logging.getLogger(__name__)
        return self.logger

    async def get_task_from_queue(self) -> Any:
        task = await self.redis_client.blpop(self.queue_names)
        self.logger.info(
            WorkerMessage.TASK_RECEIVED.value.format(
                function=self.function_name,
                data=task,
            )
        )
        return task

    async def set_task_in_queue(
            self,
            data: dict,
            queue_name: str = None,
            task_id: str = None,
    ) -> None:
        if not task_id:
            self.task_id = str(uuid.uuid4())[:FieldLength.TASK_ID.value]
        else:
            self.task_id = task_id

        if queue_name:
            queue_name += QueueStatus.PROCESSING.value
        queue = queue_name or self.queue_names[0]
        self.logger.info(
            WorkerMessage.TASK_SENT.value.format(
                queue=queue,
                task_id=self.task_id,
                data=data,
            )
        )
        task_template = dict(task_id=data)
        task_template[self.task_id] = task_template.pop('task_id')
        await self.redis_client.lpush(
            queue,
            json.dumps(task_template, ensure_ascii=False),
        )

    async def run(self):
        self.logger.info(
            WorkerMessage.WORKER_STARTED.value.format(worker=self),
        )
        if not self.function:
            self.logger.debug(WorkerMessage.NO_FUNCTION.value)
            raise RuntimeError(WorkerMessage.NO_FUNCTION.value)
        while True:
            try:
                item = await self.get_task_from_queue()
                if item:
                    queue_name, raw_data = item
                    try:
                        data = json.loads(raw_data)
                    except JSONDecodeError as e:
                        raise ValueError(
                            WorkerMessage.JSON_DECODE_ERROR.value.format(
                                error=str(e)[:FieldLength.ERROR.value]
                            ),
                        )
                    else:
                        self.logger.info(
                            WorkerMessage.DATA_RECEIVED.value.format(
                                data=data,
                                function=self.function_name,
                            )
                        )
                        task_id = list(data.keys())[0]
                        cleaned_data = list(data.values())[0]
                        await self.function(task_id, cleaned_data)
            except asyncio.CancelledError:
                self.logger.info(WorkerMessage.WORKER_STOPPED.value)
                break
            except Exception as e:
                self.logger.error(
                    WorkerMessage.PROCESSING_ERROR.value.format(
                        function=self.function_name,
                        error=str(e)[:FieldLength.ERROR.value],
                    )
                )
                await asyncio.sleep(1)
