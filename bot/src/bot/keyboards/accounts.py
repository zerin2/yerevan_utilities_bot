from dataclasses import dataclass

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.core.exceptions import EmptyUserAccountList
from bot.crud.account import user_account_crud
from bot.enums.scene_enums import SceneName
from bot.enums.utility_enums import UtilityLabel
from bot.keyboards.enums import KeyboardIcon, KeyboardText
from db.core import async_session
from db.models import UserAccount

CALLBACK_DATA_ACCOUNT_KEYBOARD = [
    SceneName.DATA.check,
    SceneName.LIST_UTILITIES.display,
    SceneName.REQUEST_READING.get,

]

EDITOR_ACCOUNT_BUTTONS = [
    (UtilityLabel.ELECTRICITY.value, SceneName.ELECTRICITY.editor),
    (UtilityLabel.GAS.value, SceneName.GAS.editor),
    (UtilityLabel.GAS_SERVICE.value, SceneName.GAS_SERVICE.editor),
    (UtilityLabel.WATER.value, SceneName.WATER.editor),
    # (Utility.VIVA_MTS.value, SceneName.VIVA_MTS.editor),
    # (Utility.TEAM_TELECOM.value, SceneName.TEAM_TELECOM.editor),
    # (Utility.U_COM.value, SceneName.U_COM.editor),
    # (Utility.OVIO.value, SceneName.OVIO.editor),
]


def add_accounts() -> InlineKeyboardMarkup:
    """ """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.ADD_ACCOUNTS.value,
                callback_data=SceneName.LIST_UTILITIES.display)],
        ],
    )


def check_or_add_or_request_account() -> InlineKeyboardMarkup:
    """ """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.CHECK_ACCOUNT.value,
                callback_data=SceneName.DATA.check)],
            [InlineKeyboardButton(
                text=KeyboardText.ADD_ACCOUNTS.value,
                callback_data=SceneName.LIST_UTILITIES.display)],
            [InlineKeyboardButton(
                text=KeyboardText.REQUEST_READING.value,
                callback_data=SceneName.REQUEST_READING.get)],
        ],
    )


async def get_icon_status_button(
        scene_name: str,
) -> KeyboardIcon | None:
    """Определяет статус кнопки для заданного типа счета.
    SceneName.editor_to_utility_name(scene_name) - получаем имя услуги (UtilityName).

    Returns:
        str: Значение иконки, отображающей статус счета. Возвращает:
            - KeyboardIcon.EMPTY.value ('⚪'), если счет не заполнен.
            - KeyboardIcon.FILLED.value ('✅'), если счет заполнен.
    """
    button_name = SceneName.editor_to_utility_name(scene_name)

    for account_name, account_value in account_values.items():
        if button_name == account_name:
            if account_value is None:
                return KeyboardIcon.EMPTY.value
            return KeyboardIcon.FILLED.value
        return None
    return None


async def display_accounts_list(user_id: str) -> InlineKeyboardMarkup:
    """Формирует клавиатуру с кнопками для редактирования счетов пользователя.

    """
    async with async_session() as session:
        user_accounts: UserAccount = await user_account_crud.get_all_accounts(
            session,
            str(user_id),
        )
    if not user_accounts:
        raise EmptyUserAccountList

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_icon_status_button(scene_name) + ' ' + text,
                    callback_data=scene_name,
                ),
            ] for text, scene_name in EDITOR_ACCOUNT_BUTTONS
        ],
    )
