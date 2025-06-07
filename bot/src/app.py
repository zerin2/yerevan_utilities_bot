import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramConflictError, TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage

import bot.main.middlewares as mw
from bot.main.errors import error_router
from bot.main.scenes.help_info import help_info_router
from bot.main.scenes.main import main_router
from logs.config import bot_logger
from settings import settings

dp = Dispatcher(storage=MemoryStorage())
dp.update.middleware(mw.RetryMiddleware())
dp.update.middleware(mw.SaveUserHistoryMiddleware())


@bot_logger.catch()
async def main() -> None:
    bot = Bot(token=settings.telegram_token)
    dp.include_routers(
        main_router,
        help_info_router,
        error_router,
    )
    try:
        bot_logger.info(f'Попытка подключения: {datetime.datetime.now()}')
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except (TelegramNetworkError, TelegramConflictError) as e:
        bot_logger.error(f'Ошибка сети или конфликт: {e}')
        await bot.session.close()
        await asyncio.sleep(2)
        await main()


if __name__ == '__main__':
    bot_logger.info('Bot Start')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot_logger.warning('Bot остановлен вручную.')
    except Exception as e:
        bot_logger.exception(f'Неожиданная ошибка: {e}')
    finally:
        bot_logger.info('Bot завершил работу.')
