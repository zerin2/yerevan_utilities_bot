import json
import uuid

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from api.enums import EndpointDescription, EndpointSummary, ResponseMessages
from api.validators import check_duplicate_accounts, get_token
from core.exceptions import RedisTaskNotFound
from core.logger_settings import logger
from schemas.message import BaseMessageData, ResultOutPutMessageData
from services.enums import LoggerMessage, StatusType
from services.utils import create_new_task, get_redis_task
from workers.tasks import check_all_task_for_completion
from workers.worker_app import rq_worker

router = APIRouter()


@router.post(
    '/start_task',
    summary=EndpointSummary.START_TASK.value,
    description=EndpointDescription.START_TASK.value,
)
async def start_task(
        message: BaseMessageData = Body(...),
        token: str = Depends(get_token),
):
    task_id = str(uuid.uuid4())[:8]
    message_data = message.model_dump()
    message_data_account = message_data.get('data')
    message_status = message_data.get('job_status')

    if message.job_status == StatusType.NEW:
        message_data['job_status'] = StatusType.PROCESSING.value
        logger.info(LoggerMessage.NEW_MESSAGE.format(
            task_id=task_id, data=message_data, status=message_status,
        ))
        try:
            check_duplicate_accounts(message_data_account)
            await create_new_task(task_id, message_data)
            for data_account in message_data_account:
                await rq_worker.set_task_in_queue(
                    task_id=task_id,
                    data=data_account,
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(
                    task_id=task_id,
                    task_status=StatusType.PROCESSING.value,
                ),
            )
        except Exception as e:
            msg = ResponseMessages.TASK_ERROR.value.format(error=str(e))
            logger.error(msg)
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=dict(
                    task_status=StatusType.ERROR.value,
                    error=msg,
                ),
            )
    logger.error(LoggerMessage.BAD_STATUS_MESSAGE.format(
        task_id=task_id,
        data=message_data,
        status=message_status,
    ))
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content=ResponseMessages.INVALID_STATUS.value.format(
            status=message_status,
        ),
    )


@router.get(
    '/result/{task_id}',
    response_model=ResultOutPutMessageData,
    summary=EndpointSummary.RESULT.value,
    description=EndpointDescription.RESULT.value,
)
async def get_result(
        task_id: str,
        token: str = Depends(get_token),
):
    try:
        if not await check_all_task_for_completion(task_id):
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content=dict(
                    task_status=StatusType.PROCESSING.value,
                    message=ResponseMessages.TASK_IN_PROGRESS.value.format(
                        task_id=task_id,
                    ),
                ),
            )
        data = json.loads(await get_redis_task(task_id))
    except RedisTaskNotFound as e:
        logger.error(ResponseMessages.TASK_NOT_FOUND.format(task_id=task_id))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(
                task_status=StatusType.ERROR.value,
                error=str(e),
            ),
        )
    except Exception as e:
        msg = ResponseMessages.RESULT_ERROR.value.format(error=str(e))
        logger.exception(msg)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=dict(
                task_status=StatusType.ERROR.value,
                error=msg,
            ),
        )
    else:
        logger.info(ResponseMessages.TASK_FOUND.format(task_id=task_id))
        return data
