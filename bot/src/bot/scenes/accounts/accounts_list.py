from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message
from enums.profile_enums import BotMessage
from enums.scene_enums import SceneName

import bot.main.keyboards as kb


class ListUtilitiesAccountsScene(Scene, state=SceneName.LIST_UTILITIES.display):
    """Сцена вывода списка типов счетов."""

    @on.callback_query.enter()
    @on.message.enter()
    async def handle_list(self, event: Message | CallbackQuery) -> None:
        user_id = event.from_user.id
        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.answer(
                BotMessage.CHOOSE_ACCOUNTS_IN_LIST.value,
                reply_markup=await kb.display_accounts_list(str(user_id)),
            )
        else:
            await event.answer(
                BotMessage.CHOOSE_ACCOUNTS_IN_LIST.value,
                reply_markup=await kb.display_accounts_list(str(user_id)),
            )

    @on.callback_query(F.data.in_([button[1] for button in kb.EDITOR_ACCOUNT_BUTTONS]))
    async def handle_account_selection(self, callback: CallbackQuery) -> None:
        await callback.answer()
        await self.wizard.goto(callback.data)
        await callback.message.delete()
