from aiogram import F, Router
from aiogram.types import Message

from bot.enums.profile_enums import BotMessage

error_router = Router()


@error_router.message(F.text.startswith('/'))
async def unknown_cmd(message: Message) -> None:
    return message.reply(BotMessage.UNKNOWN.value)


@error_router.message()
async def unknown_msg(message: Message) -> None:
    return message.reply(BotMessage.UNKNOWN.value)
