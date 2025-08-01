from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from bot.core.exceptions import EmptyUserAccountList
from bot.enums.profile_enums import BotMessage
from bot.enums.scene_enums import EDITOR_AVAILABLE_SCENE_NAMES, SceneName
from bot.keyboards.accounts import display_accounts_list
from logs.config import bot_logger


class ListUtilitiesAccountsScene(
    Scene,
    state=SceneName.LIST_UTILITIES.display,
):
    """Сцена вывода списка типов счетов."""

    @on.callback_query.enter()
    @on.message.enter()
    async def handle_list(self, event: Message | CallbackQuery) -> None:
        user_id = str(event.from_user.id)
        try:
            if isinstance(event, CallbackQuery):
                await event.answer()
                await event.message.answer(
                    BotMessage.CHOOSE_ACCOUNTS_IN_LIST.value,
                    reply_markup=await display_accounts_list(user_id),
                )
            else:
                await event.answer(
                    BotMessage.CHOOSE_ACCOUNTS_IN_LIST.value,
                    reply_markup=await display_accounts_list(user_id),
                )
        except EmptyUserAccountList as e:
            error_name = e.__class__.__name__
            bot_logger.error(f'{error_name}, user_id={user_id}')
            await event.answer()
            await event.message.answer(f'Ошибка: "{error_name}"')
            await event.message.answer(BotMessage.ERROR_LIST_ACCOUNT.value)

    @on.callback_query(
        # F.data.in_([button[1] for button in EDITOR_ACCOUNT_BUTTONS]),
        F.data.in_(EDITOR_AVAILABLE_SCENE_NAMES),  # todo проверить работоспособность
    )
    async def handle_account_selection(self, callback: CallbackQuery) -> None:
        await callback.answer()
        await self.wizard.goto(callback.data)
        await callback.message.delete()
