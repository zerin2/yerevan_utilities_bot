import json

from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
)

from core.exceptions import (
    Account404,
    CustomBaseException,
    JsonError,
    Selector404,
    StatusError,
    ValidationError,
)
from core.logger_settings import logger
from services.enums import StatusType
from services.parser.app import Parser
from services.utils import (
    change_job_status,
    get_redis_task,
    patch_account_data_by_id,
)

ERROR_LEN_MSG = 100


async def check_all_task_for_completion(task_id: str) -> bool:
    raw = await get_redis_task(task_id)
    try:
        task_data = json.loads(raw)
    except json.JSONDecodeError:
        msg = f'Ошибка при декодировании JSON для task_id={task_id}'
        logger.error(msg)
        raise JsonError(msg)
    list_tasks = task_data.get('data')
    for task in list_tasks:
        if task.get('status_response') in (StatusType.NEW.value, None):
            return False
    return True


async def forming_error_response(
        task_id: str,
        data: dict,
        _exception: RetryError | Exception,
        retry_exception: bool = False,
) -> None:
    if retry_exception:
        original_exception = _exception.last_attempt.exception()
        error_class_name = original_exception.__class__.__name__
        error_message = str(original_exception)[:ERROR_LEN_MSG]
        logger.error(f'{error_message}')
    else:
        error_class_name = _exception.__class__.__name__
        error_message = str(_exception)[:ERROR_LEN_MSG]
        logger.error(f'{error_message}')
    return (
        await patch_account_data_by_id(
            task_id=task_id,
            account=data.get('account'),
            status_response=StatusType.ERROR.value,
            key='response',
            value=dict(
                error=error_class_name,
                message=error_message,
            ),
        )
    )


@retry(
    retry=retry_if_exception_type(Selector404),
    stop=stop_after_attempt(3),
)
async def parser_run_with_retry(parser: Parser) -> dict:
    logger.debug('>>> Вызов parser.run() внутри retry')
    return await parser.run()


async def start_parsing(task_id: str, data: dict) -> dict:
    logger.info(f'Worker выполняет: task_id: {task_id}, data: {data}')
    try:
        parser = Parser(message_data=data)
        result_data = await parser_run_with_retry(parser)
        await patch_account_data_by_id(
            task_id=task_id,
            account=data.get('account'),
            status_response=StatusType.COMPLETE.value,
            key='response',
            value=result_data,
        )
    except Account404 as e:
        await forming_error_response(
            task_id=task_id,
            data=data,
            _exception=e,
        )
    except RetryError as e:
        await forming_error_response(
            task_id=task_id,
            data=data,
            _exception=e,
            retry_exception=True,
        )
    except (
            Selector404,
            ValidationError,
            StatusError,
            CustomBaseException,
            Exception,
    ) as e:
        await forming_error_response(
            task_id=task_id,
            data=data,
            _exception=e,
        )
    finally:
        if await check_all_task_for_completion(task_id):
            await change_job_status(task_id, StatusType.COMPLETE.value)
            logger.info(
                f'Все подзадачи по task_id={task_id} завершены.',
            )
