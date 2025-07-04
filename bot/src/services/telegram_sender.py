import asyncio
from dataclasses import dataclass

import aiogram.exceptions as exc
from aiogram import Bot

from bot.crud.user import user_crud
from bot.enums.setting_enums import FieldLength, SendTelegramError
from db.core import async_session
from db.models.models import UserProfile
from logs.config import worker_logger
from settings import settings

LITE_RETRY_DELAY = 2


@dataclass
class BotSender:
    """Класс для безопасной отправки сообщений пользователям Telegram с автоматической
    обработкой ошибок и сохранением статуса доставки.

    Атрибуты:
        bot (Bot): Экземпляр Telegram-бота (инициализируется автоматически).
        telegram_id (str | int): Telegram ID пользователя,
        которому отправляется сообщение.
        message (str): Текст отправляемого сообщения.

    Поведение:
        - При временных ошибках (сетевые, ограничение по времени)
        повторяет отправку с задержкой.
        - При критических ошибках (бот заблокирован, пользователь удалён и т.д.)
         прекращает отправку и записывает статус ошибки в базу данных.
        - Всегда закрывает сессию бота после завершения попыток отправки.

    Методы:
        send_message(): Асинхронно отправляет сообщение,
        обрабатывает ошибки и сохраняет результат.
    """

    bot: Bot = None
    telegram_id: str | int = None
    message: str = None

    def __post_init__(self):
        self.bot = Bot(token=settings.telegram_token)
        self.message = str(self.message)

    async def send_message(self):
        error_msg = (
            '{error_cls} Ошибка отправки '
            'сообщения пользователю: {telegram_id}, ошибка: {e}'
        )
        success_msg = (
            'Сообщение отправлено. '
            'UserID: {telegram_id}, сообщение: {message}'
        )
        user_404 = (
            'Ошибка отправки сообщения, '
            'пользователь не найден: {telegram_id}'
        )
        try:
            while True:
                try:
                    await self.bot.send_message(
                        int(self.telegram_id), self.message,
                    )
                    worker_logger.info(success_msg.format(
                        telegram_id=str(self.telegram_id),
                        message=self.message,
                    ))
                    return
                except SendTelegramError.LITE_ERRORS.value as e:
                    worker_logger.error(error_msg.format(
                        error_cls=e.__class__.__name__,
                        telegram_id=str(self.telegram_id),
                        e=e,
                    ))
                    await asyncio.sleep(
                        e.retry_after
                        if isinstance(e, exc.TelegramRetryAfter)
                        else LITE_RETRY_DELAY,
                    )
                except SendTelegramError.CRITICAL_ERRORS.value as e:
                    async with async_session() as session:
                        user_obj: UserProfile = await user_crud.get_user_by_tg_id(
                            session, str(self.telegram_id),
                        )
                        if user_obj is not None:
                            user_obj.is_delivery_blocked = True
                            user_obj.delivery_blocked_error = str(
                                e.__class__.__name__,
                            )[:FieldLength.DELIVERY_ERROR.value]
                            await session.commit()
                        else:
                            worker_logger.error(user_404.format(
                                telegram_id=str(self.telegram_id),
                            ))
                    worker_logger.error(error_msg.format(
                        error_cls=e.__class__.__name__,
                        telegram_id=str(self.telegram_id),
                        e=e,
                    ))
                    break
        finally:
            await self.bot.session.close()

# async def main():
#     a = BotSender(tg_id=259564426, message='куку')
#     for i in range(5):
#         await a.send_message()
#
#
# asyncio.run(main())
