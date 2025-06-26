from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.enums.notice_enums import NoticeInterval, NoticeState, NoticeType
from bot.enums.scene_enums import SceneName
from bot.keyboards.enums import KeyboardText


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
                    text=NoticeState.to_human(state.value),
                    callback_data=state.value,
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
    return InlineKeyboardMarkup(
        inline_keyboard=[[button] for button in buttons],
    )


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
    """Создаёт список списков кнопок для отображения клавиатуры
    с интервалами времени.

    Args:
        n_rows (int): Количество кнопок в каждой строке клавиатуры.
        flag (str): флаг для определения сцены.

    Returns:
        list[list[InlineKeyboardButton]]: Список строк клавиатуры,
        каждая из которых содержит до `n_rows` кнопок.

    """
    buttons = [
        InlineKeyboardButton(
            text=NoticeInterval.to_human(interval.value),
            callback_data=interval.name + (
                start_flag()
                if flag == 'start'
                else end_flag()
            ),
        )
        for interval in NoticeInterval
    ]
    return list(chunks(buttons, n_rows))


def display_notice_hours(rows: int, flag: str) -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с выбором времени оповещения.
    (flag: start | end)
    """
    return InlineKeyboardMarkup(
        inline_keyboard=list_notice_hours(rows, flag),
    )
