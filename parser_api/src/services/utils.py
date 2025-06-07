import json

from core.cache_settings import redis_client
from core.exceptions import RedisTaskNotFound
from core.logger_settings import logger
from services.enums import TTL, StatusType


async def create_new_task(task_id: str, data: dict) -> None:
    return await redis_client.set(
        task_id,
        json.dumps(data),
        ex=TTL.REDIS_KEY.value,
    )


async def get_redis_task(task_id: str) -> str:
    redis_task = await redis_client.get(task_id)
    if redis_task is None:
        msg = f'Задача с task_id={task_id} не найдена.'
        logger.debug(msg)
        raise RedisTaskNotFound(msg)
    return redis_task


async def change_job_status(task_id: str, status: StatusType) -> None:
    redis_raw = await get_redis_task(task_id)
    redis_task = json.loads(redis_raw)
    redis_task['job_status'] = status
    await redis_client.set(
        task_id,
        json.dumps(redis_task),
        ex=TTL.REDIS_KEY.value,
    )


async def patch_account_data_by_id(
        task_id: str,
        account: str,
        key: str,
        value: str,
        status_response: StatusType = None,
) -> None:
    redis_raw = await get_redis_task(task_id)
    full_data = json.loads(redis_raw)
    data_list = full_data.get('data')
    for data in data_list:
        if data.get('account') == account:
            if status_response:
                data['status_response'] = status_response
            data[key] = value
            break
    await redis_client.set(
        task_id,
        json.dumps(full_data),
        ex=TTL.REDIS_KEY.value,
    )
