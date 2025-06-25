import asyncio
from dataclasses import dataclass

import aiogram.exceptions as exc
from aiogram import Bot

from bot.manager.composite_manager import CompositeManager
from db.core import async_session
from logs.config import worker_logger
from settings import settings

LITE_RETRY_DELAY = 2
LITE_ERRORS = (exc.TelegramNetworkError, exc.TelegramRetryAfter)
CRITICAL_ERRORS = (
    exc.TelegramNotFound,
    exc.TelegramUnauthorizedError,
    exc.TelegramForbiddenError,
    Exception,
)


@dataclass
class BotSender:
    """Класс для безопасной отправки сообщений пользователям Telegram с автоматической
    обработкой ошибок и сохранением статуса доставки.

    Атрибуты:
        bot (Bot): Экземпляр Telegram-бота (инициализируется автоматически).#
        tg_id (str | int): Telegram ID пользователя, которому отправляется сообщение.#
        message (str): Текст отправляемого сообщения.

    Поведение:
        - При временных ошибках (сетевые, ограничение по времени) повторяет отправку с задержкой.
        - При критических ошибках (бот заблокирован, пользователь удалён и т.д.)
         прекращает отправку и записывает статус ошибки в базу данных (`is_delivery_blocked`).
        - Всегда закрывает сессию бота после завершения попыток отправки.

    Методы:
        send_message(): Асинхронно отправляет сообщение,
        обрабатывает ошибки и сохраняет результат.
    """

    bot: Bot = None
    tg_id: str | int = None
    message: str = None

    def __post_init__(self):
        self.bot = Bot(token=settings.telegram_token)
        self.tg_id = int(self.tg_id)
        self.message = str(self.message)

    async def send_message(self):
        error_msg = (
            '{error_cls} Ошибка отправки '
            'сообщения пользователю: {tg_id}, ошибка: {e}'
        )
        success_msg = (
            'Сообщение отправлено. '
            'UserID: {tg_id}, сообщение: {message}'
        )
        try:
            while True:
                try:
                    await self.bot.send_message(self.tg_id, self.message)
                    worker_logger.info(success_msg.format(
                        tg_id=self.tg_id,
                        message=self.message,
                    ))
                    return
                except LITE_ERRORS as e:
                    worker_logger.error(error_msg.format(
                        error_cls=e.__class__.__name__,
                        tg_id=self.tg_id,
                        e=e,
                    ))
                    await asyncio.sleep(
                        e.retry_after
                        if isinstance(e, exc.TelegramRetryAfter)
                        else LITE_RETRY_DELAY,
                    )
                except CRITICAL_ERRORS as e:
                    async with async_session() as session:
                        user_repo = CompositeManager(session)
                        await user_repo.edit_one_value(
                            user_repo.USER_PROFILE_MODEL,
                            'telegram_id',
                            str(self.tg_id),
                            'is_delivery_blocked',
                            str(e.__class__.__name__),
                        )
                        await session.commit()
                    worker_logger.error(error_msg.format(
                        error_cls=e.__class__.__name__,
                        tg_id=self.tg_id,
                        e=e,
                    ))
                    break
        finally:
            await self.bot.session.close()

# async def main():
#     a = BotSender(tg_id=259564426, message='куку')
#     for i in range(50):
#         await a.send_message()
#
#
# asyncio.run(main())


# {'tg_id': '259564426',
# 'task_id': '3f335481',
# 'count': 3,
# 'status':  'complete',
# 'notify': True,
# 'account': '0390315',
# 'account_type': 'code',
# 'utility': 'electricity',
# 'first_check': False,
# 'response':
# {'address': 'ք.ԵՐԵՎԱՆ ԳԱՐԵԳԻՆ ՆԺԴԵՀԻ փող., 5, 15',
# 'traffic': 'Ց-2.680, Գ-1.200/3561.630', 'debit': '0', 'credit': '332.55'}}

# {'tg_id': '259564426',
# 'task_id': '435148b3',
# 'count': 3,
# 'status': 'error',
# 'notify': True,
# 'account': '12321312',
# 'account_type': 'code',
# 'utility': 'gas',
# 'first_check': False,
# 'response': '(Account404) Аккаунт не найден'}
