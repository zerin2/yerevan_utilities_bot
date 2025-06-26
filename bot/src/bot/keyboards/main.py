from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.keyboards.enums import KeyboardCMD, KeyboardText


def main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=KeyboardText.UPDATE_DEBT.value),
             KeyboardButton(text=KeyboardText.CHECK_DEBT.value)],
            [KeyboardButton(text=KeyboardText.CHANGE_ID.value),
             KeyboardButton(text=KeyboardText.SETTINGS.value)],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def mini_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=KeyboardText.CHANGE_ID.value),
             KeyboardButton(text=KeyboardText.SETTINGS.value)],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def display_debt() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.CHECK_DEBT.value,
                callback_data=KeyboardCMD.CHECK_DEBT.value,
            )],
        ],
    )
