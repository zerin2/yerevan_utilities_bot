import inspect
import logging
from typing import Callable

from loguru import logger

from settings import (
    BOT_LOG_PATH,
    PROVIDERS_LOG_PATH,
    WORKER_LOG_PATH,
)


class InterceptHandler(logging.Handler):
    """Хэндлер, который перехватывает сообщения от стандартных логгеров
    и направляет их в глобальный синк Loguru (`global_logger`).
    """

    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = bot_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = inspect.currentframe(), 0
        while frame and (
                depth == 0 or frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back
            depth += 1
        (
            bot_logger
            .bind(logger_name=record.name)
            .opt(depth=depth, exception=record.exc_info)
            .log(level, record.getMessage())
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def filter_category(name_category: str) -> Callable:
    """Фильтр для категории раздела и виду ошибки."""
    return lambda record: record['extra'].get('category') == name_category


bot_logger = logger.bind(category='bot')
bot_logger.add(
    BOT_LOG_PATH,
    rotation='10 MB',
    enqueue=True,
    backtrace=True,
    filter=filter_category('bot'),
)
providers_logger = logger.bind(category='providers')
providers_logger.add(
    PROVIDERS_LOG_PATH,
    rotation='10 MB',
    enqueue=True,
    backtrace=True,
    filter=filter_category('providers'),
)
worker_logger = logger.bind(category='worker')
worker_logger.add(
    WORKER_LOG_PATH,
    rotation='10 MB',
    enqueue=True,
    backtrace=True,
    filter=filter_category('worker'),
)
