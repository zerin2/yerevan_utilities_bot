from bot.crud.account import (
    AccountBotManager,
    AccountsDetailsBotManager,
    UtilitiesTypeBotManager,
)
from bot.crud.feedback import FeedbackBotManger
from bot.crud.users import UserBotManager


class CompositeManager(
    AccountBotManager,
    AccountsDetailsBotManager,
    UtilitiesTypeBotManager,
    FeedbackBotManger,
    UserBotManager,
):
    """CompositeManager объединяет функционал всех менеджеров:
    - UserManager: пользователи.
    - AccountBotManager: счета.
    - UtilitiesTypeBotManager: типы коммунальных услуг.
    - AccountsDetailsBotManager: коммунальные счета пользователя.
    - FeedbackBotManger: обработка отзывов и ошибок.
    """
