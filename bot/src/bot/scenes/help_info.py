from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.enums.profile_enums import BotMessage, BotWords

help_info_router = Router()


@help_info_router.message(Command('info'))
async def info_cmd(message: Message):
    return message.reply(BotMessage.INFO.value)


@help_info_router.message(Command('help'))
async def help_cmd(message: Message):
    return message.reply(BotMessage.HELP.value)


@help_info_router.message(F.text.lower().in_(BotWords.HELP.value))
async def help_msg(message: Message):
    return message.reply(BotMessage.HELP.value)


@help_info_router.message(Command('about'))
async def about_cmd(message: Message):
    return message.reply(BotMessage.ABOUT_BOT.value)
