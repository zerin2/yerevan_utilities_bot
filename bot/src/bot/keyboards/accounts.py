from dataclasses import dataclass

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.crud._composite_manager import CompositeManager
from bot.enums.scene_enums import SceneName
from bot.enums.utility_enums import UtilityNameIcon
from bot.keyboards.enums import KeyboardIcon, KeyboardText
from db.core import async_session

CALLBACK_DATA_ACCOUNT_KEYBOARD = [
    SceneName.DATA.check,
    SceneName.LIST_UTILITIES.display,
    SceneName.REQUEST_READING.get,

]

EDITOR_ACCOUNT_BUTTONS = [
    (UtilityNameIcon.ELECTRICITY.value, SceneName.ELECTRICITY.editor),
    (UtilityNameIcon.GAS.value, SceneName.GAS.editor),
    (UtilityNameIcon.GAS_SERVICE.value, SceneName.GAS_SERVICE.editor),
    (UtilityNameIcon.WATER.value, SceneName.WATER.editor),
    # (Utility.VIVA_MTS.value, SceneName.VIVA_MTS.editor),
    # (Utility.TEAM_TELECOM.value, SceneName.TEAM_TELECOM.editor),
    # (Utility.U_COM.value, SceneName.U_COM.editor),
    # (Utility.OVIO.value, SceneName.OVIO.editor),
]


@dataclass
class KeyboardStatusAccount:
    """Класс для работы со статусами счетов пользователя и генерации статуса кнопок.

    Attributes:
        user_id (str): Telegram ID пользователя.

    """

    user_id: str

    async def get_account_values(self) -> dict:
        """Получает значения всех счетов пользователя из базы данных.

        Returns:
            dict: Словарь, где ключи - типы счетов (напр. "electricity"),
            а значения - текущие данные счета. Возвращает пустой словарь, если данных нет.

        """
        async with async_session() as session:
            user_repo = CompositeManager(session)
            account_values = await user_repo.get_all_account_by_tg_id(
                str(self.user_id),
            )
            return account_values or {}

    async def get_status_button(self, button: str) -> bool:
        """Определяет статус кнопки для заданного типа счета.
        SceneName.to_utility_name(button) - получаем имя модели по названию callback_data.

        Args:
            button (str): Название кнопки (тип счета).

        Returns:
            str: Значение иконки, отображающей статус счета. Возвращает:
                - KeyboardIcon.EMPTY.value ('⚪'), если счет не заполнен.
                - KeyboardIcon.FILLED.value ('✅'), если счет заполнен.

        """
        if button is None:
            button = ''

        account_values = await self.get_account_values()
        button_name = SceneName.to_utility_name(button)
        for account_name, account_value in account_values.items():
            if button_name == account_name:
                if account_value is None:
                    return KeyboardIcon.EMPTY.value
                return KeyboardIcon.FILLED.value
            return None
        return None


def add_accounts() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.ADD_ACCOUNTS.value,
                callback_data=SceneName.LIST_UTILITIES.display)],
        ],
    )


async def display_accounts_list(user_id: str) -> InlineKeyboardMarkup:
    """Формирует клавиатуру с кнопками для редактирования счетов пользователя.

    Args:
        user_id (str): Telegram ID пользователя.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками, где каждая кнопка
        отображает статус (пустой или заполненный) соответствующего счета.

    """
    keyboard_repo = KeyboardStatusAccount(user_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await keyboard_repo.get_status_button(data) + ' ' + text,
                    callback_data=data,
                ),
            ] for text, data in EDITOR_ACCOUNT_BUTTONS
        ],
    )


def check_or_add_or_request_account() -> InlineKeyboardMarkup:
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
