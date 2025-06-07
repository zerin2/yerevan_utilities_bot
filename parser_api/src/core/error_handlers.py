from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar

from fastapi import status
from fastapi.responses import JSONResponse

from core.logger_settings import logger

F = TypeVar('F', bound=Callable[..., Awaitable[Any]])


def handle_errors(func: F) -> F:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={'error': str(e)},
            )

    return wrapper
