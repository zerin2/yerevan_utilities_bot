from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.enums.scene_enums import SceneName
from bot.keyboards.enums import KeyboardText


def feedback_additional() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.USUAL_REVIEW.value,
                callback_data=SceneName.USUAL_REVIEW.editor)],
            [InlineKeyboardButton(
                text=KeyboardText.FOUND_ERROR.value,
                callback_data=SceneName.FOUND_ERROR.editor)],
        ],
    )
