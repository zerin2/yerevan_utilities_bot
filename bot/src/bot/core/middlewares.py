import asyncio
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.types import Update
from typing_extensions import Awaitable

from bot.crud.user_history import user_history_crud
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
    """Middleware для автоматического сохранения истории действий пользователя в дб.

    Описание:
        - Каждый раз при обработке события (сообщения пользователя) сохраняет
        ключевую информацию (user_id, chat_id, message_id, текст сообщения,
        состояние пользователя) в таблицу истории.
        - В случае возникновения ошибок сохраняет подробное сообщение
        в лог (уровень CRITICAL), не прерывая обработку запроса.

    Параметры:
        handler: Callable
            Функция-обработчик события, которая будет вызвана дальше по цепочке middleware.
        event: Any
            Событие (например, Message), содержащее информацию о входящем сообщении.
        data: dict
            Словарь с дополнительными данными, доступными для middleware и хендлеров.

    Сохраняет в базу:
        - user_id: ID пользователя Telegram
        - chat_id: ID чата
        - message_id: ID сообщения
        - message_content: текст сообщения
        - state: текущее состояние FSMContext (если есть)

    Обработка ошибок:
        - В случае возникновения исключения, пишет критическую ошибку в лог,
          но не прерывает дальнейшее выполнение цепочки хендлеров.
    """

    async def __call__(self, handler, event, data, **kwargs) -> Any:
        tg_handler = await handler(event, data)
        try:
            message = getattr(event, 'message', None)
            from_user = getattr(message, 'from_user', None)
            data_state = data.get('state', '')
            user_state = await data_state.get_state()  # noqa
            if from_user and message:
                async with async_session() as session:
                    await user_history_crud.write_history(
                        session=session,
                        message=message,
                        state=user_state,
                    )
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
