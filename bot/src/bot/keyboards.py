from dataclasses import dataclass
from enum import Enum

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from enums.scene_enums import SceneName, Utility
from enums.setting_enums import NoticeInterval, NoticeState, NoticeType

from bot.crud.composite_manager import CompositeManager
from db.core import async_session

CALLBACK_DATA_ACCOUNT_KEYBOARD = [
    SceneName.DATA.check,
    SceneName.LIST_UTILITIES.display,
    SceneName.REQUEST_READING.get,

]
EDITOR_ACCOUNT_BUTTONS = [
    (Utility.ELECTRICITY.value, SceneName.ELECTRICITY.editor),
    (Utility.GAS.value, SceneName.GAS.editor),
    (Utility.GAS_SERVICE.value, SceneName.GAS_SERVICE.editor),
    (Utility.WATER.value, SceneName.WATER.editor),
    # (Utility.VIVA_MTS.value, SceneName.VIVA_MTS.editor),
    # (Utility.TEAM_TELECOM.value, SceneName.TEAM_TELECOM.editor),
    # (Utility.U_COM.value, SceneName.U_COM.editor),
    # (Utility.OVIO.value, SceneName.OVIO.editor),
]


class KeyboardText(Enum):
    CHECK_DEBT = 'Мои счета 🧾'
    UPDATE_DEBT = 'Обновить задолженность 🔄'
    ADD_ACCOUNTS = 'Добавить лицевой счет 📋'
    CHANGE_ID = 'Добавить/изменить лицевой счет ✏️'
    SETTINGS = 'Настройки ⚙️'
    REQUEST_READING = 'Запросить показания 📩'
    CHANGE_NOTICE_INTERVAL = 'Изменить интервал уведомлений 🕒'
    CHANGE_NOTICE_STATE = 'Вкл./Выкл. уведомления 🔔'
    USUAL_REVIEW = 'Отзыв или пожелание 💬'
    FOUND_ERROR = 'Сообщить об ошибке ⚠️'
    CHECK_ACCOUNT = 'Проверить лицевой счет 👀'


class KeyboardCMD(Enum):
    CHECK_DEBT = 'check_debt'
    UPDATE_DEBT = 'update_debt'
    ADD_ACCOUNTS = 'add_accounts'
    CHANGE_ID = 'change_id'
    SETTINGS = 'settings'


class KeyboardIcon(Enum):
    EMPTY = '⚪'
    FILLED = '✅'


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
            account_values = await user_repo.get_all_account_by_tg_id(str(self.user_id))
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


def add_accounts() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.ADD_ACCOUNTS.value,
                callback_data=SceneName.LIST_UTILITIES.display)],
        ],
    )


def display_debt() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=KeyboardText.CHECK_DEBT.value,
                                  callback_data=KeyboardCMD.CHECK_DEBT.value)],
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


def change_setting_interval_notice() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=KeyboardText.CHANGE_NOTICE_STATE.value,
                callback_data=SceneName.NOTICE_STATE.editor)],
            [InlineKeyboardButton(
                text=KeyboardText.CHANGE_NOTICE_INTERVAL.value,
                callback_data=SceneName.NOTICE_INTERVAL.editor)],
        ],
    )


def display_notice_state() -> InlineKeyboardMarkup:
    """
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=NoticeState.to_human(state.value),  # noqa
                    callback_data=state.value  # noqa
                ),
            ] for state in NoticeState
        ],
    )


def display_notice_type() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с типами оповещений.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками,
        соответствующими типам оповещений.

    """
    buttons = []
    for interval in NoticeType:
        text = NoticeType.to_human(interval.value)  # noqa
        value = interval.value  # noqa
        if value == NoticeType.PERIOD.value:
            text += ' укажите необходимый'
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=value,
        ))
    return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


def chunks(lst: list, n: int):
    """Разбивает список на части (чанки) длиной `n` элементов.

    info: range(start, stop, step)

    Args:
        lst (list): Исходный список, который нужно разбить.
        n (int): Количество элементов в каждом чанке (группе).

    Yields:
        list: Подсписок длиной до `n` элементов.

    Пример:
    1)
    lst = ['a', 'b', 'c', 'd', 'e', 'f']
    n = 2
    result:
    i = 0  → chunk = lst[0:2] → ['a', 'b']
    i = 2  → chunk = lst[2:4] → ['c', 'd']
    i = 4  → chunk = lst[4:6] → ['e', 'f']
    ...
    [['a', 'b'], ['c', 'd'], ['e', 'f']]

    2)
        list(chunks([1, 2, 3, 4, 5], 2))
        ...
        [[1, 2], [3, 4], [5]]

    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def start_flag() -> str:
    return '_start'


def end_flag() -> str:
    return '_end'


def list_notice_hours(n_rows: int, flag: str):
    """Создаёт список списков кнопок для отображения клавиатуры с интервалами времени.

    Args:
        n_rows (int): Количество кнопок в каждой строке клавиатуры.
        flag (str): флаг для определения сцены.

    Returns:
        list[list[InlineKeyboardButton]]: Список строк клавиатуры,
        каждая из которых содержит до `n_rows` кнопок.

    """
    buttons = [
        InlineKeyboardButton(
            text=NoticeInterval.to_human(interval.value),  # noqa
            callback_data=interval.name + (start_flag() if flag == 'start' else end_flag())  # noqa
        )
        for interval in NoticeInterval
    ]
    return list(chunks(buttons, n_rows))


def display_notice_hours(rows: int, flag: str) -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с выбором времени оповещения. flag: start | end"""
    return InlineKeyboardMarkup(inline_keyboard=list_notice_hours(rows, flag))


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
