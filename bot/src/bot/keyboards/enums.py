from enum import Enum


class KeyboardText(str, Enum):
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


class KeyboardCMD(str, Enum):
    CHECK_DEBT = 'check_debt'
    UPDATE_DEBT = 'update_debt'
    ADD_ACCOUNTS = 'add_accounts'
    CHANGE_ID = 'change_id'
    SETTINGS = 'settings'


class KeyboardIcon(str, Enum):
    EMPTY = '⚪'
    FILLED = '✅'
