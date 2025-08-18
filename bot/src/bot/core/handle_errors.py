import json
from functools import wraps
from typing import Any

from sqlalchemy.exc import (
    IntegrityError,
    InvalidRequestError,
    NoResultFound,
    SQLAlchemyError,
    StatementError,
)

from logs.config import bot_logger

LOGGER = bot_logger


def handle_db_errors(func, logger: Any = None):
    """Обработка исключений при работе с БД (для async-функций)."""
    logger = logger or LOGGER

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            logger.warning(
                f'IntegrityError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except StatementError as e:
            logger.exception(
                f'Передаются некорректные параметры\n'
                f'StatementError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except NoResultFound as e:
            logger.exception(
                f'NoResultFound '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except InvalidRequestError as e:
            logger.exception(
                f'Запрос выполнен с нарушением '
                f'логики SQLAlchemy\n'
                f'InvalidRequestError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except SQLAlchemyError as e:
            logger.exception(
                f'SQLAlchemyError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except ConnectionError as e:
            logger.critical(
                f'Потеря соединения с базой данных '
                f'или проблемы на стороне сервера,\n'
                f'ConnectionError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except ValueError as e:
            logger.warning(
                f'ValueError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except Exception as e:
            logger.exception(
                f'Неизвестная ошибка '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise

    return wrapper


def handle_json_errors(func, logger=LOGGER):
    """Обработка исключений, которые могут возникнуть
    при обработке json. Декоратор применяется к
    асинхронным функциям.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.exception(
                f'Файл по указанному пути не найден или '
                f'не может быть создан\n'
                f'FileNotFoundError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except PermissionError as e:
            logger.exception(
                f'Нет прав доступа для чтения/записи файла\n'
                f'PermissionError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except UnicodeDecodeError as e:
            logger.exception(
                f'Файл содержит символы, '
                f'которые не могут быть декодированы в utf-8\n'
                f'UnicodeDecodeError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except json.JSONDecodeError as e:
            logger.exception(
                f'Попытка десериализовать строку, '
                f'которая не является корректным JSON\n'
                f'json.JSONDecodeError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except IntegrityError as e:
            logger.warning(
                f'IntegrityError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except TypeError as e:
            logger.exception(
                f'Объект, который не поддерживается JSON\n'
                f'TypeError '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise
        except Exception as e:
            logger.exception(
                f'Неизвестная ошибка '
                f'in {func.__name__} {args}, {kwargs}: {str(e)}',
            )
            raise

    return wrapper
