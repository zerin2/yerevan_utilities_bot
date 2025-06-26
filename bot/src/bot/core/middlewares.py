import asyncio
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.types import Update
from typing_extensions import Awaitable

from bot.crud._composite_manager import CompositeManager
from db.core import async_session
from logs.config import bot_logger


class CustomBaseMiddleware(BaseMiddleware):
    """Базовый промежуточный слой для обработки событий."""

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
            **kwargs,
    ) -> Any:
        return await handler(event, data)


class SaveUserHistoryMiddleware(CustomBaseMiddleware):
    """Сохраняет историю запросов в бд."""

    async def __call__(self, handler, event, data, **kwargs) -> Any:
        tg_handler = await handler(event, data)
        try:
            message = getattr(event, 'message', None)
            from_user = getattr(message, 'from_user', None)
            data_state = data.get('state', '')
            user_state = await data_state.get_state()  # noqa
            if from_user and message:
                user_tg_id = from_user.id
                async with async_session() as session:
                    user_repo = CompositeManager(session)
                    await user_repo.add_user_if_not_exists(str(user_tg_id))
                    await user_repo.write_history(message=message, state=user_state)
                    await session.commit()
        except Exception as e:
            bot_logger.critical(
                f'{e.__class__.__name__} !ERROR! save user\'s history: {str(e)}',
            )
        return tg_handler


class RetryMiddleware(CustomBaseMiddleware):
    """Обработчик лимита и задержки отправки сообщений от бота."""

    @staticmethod
    async def exception_handler(exception, from_user, message, timer) -> None:
        bot_logger.error(
            f'{exception.__class__.__name__} !ERROR! user: {from_user.id}, '
            f'message: {message}, timer: {timer}',
        )
        await asyncio.sleep(timer)

    async def __call__(self, handler, event, data, **kwargs) -> Any:
        max_retries = 10
        default_timer = 3
        message = getattr(event, 'message', None)
        from_user = getattr(message, 'from_user', None)
        for retry in range(max_retries):
            try:
                tg_handler = await handler(event, data)
                return tg_handler
            except TelegramRetryAfter as e:
                await self.exception_handler(e, from_user, message, e.retry_after)
            except TelegramNetworkError as e:
                await self.exception_handler(e, from_user, message, default_timer)
        bot_logger.critical(
            f'!ERROR! '
            f'не удалось отправить сообщение после {max_retries} попыток, '
            f'user: {from_user.id}, message: {message}',
        )
        return None
