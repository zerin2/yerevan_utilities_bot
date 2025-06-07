from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message
from enums.profile_enums import BotMessage
from enums.scene_enums import SceneName

from bot.manager.composite_manager import CompositeManager
from db.core import async_session


class GetDataAccountScene(Scene, state=SceneName.DATA.get):
    """  """

    @on.message.enter()
    async def handle_enter(self, message: Message) -> None:
        await message.answer(
            BotMessage.ACCOUNT_DATA_HEAD.value
            +
            BotMessage.ACCOUNT_DATA_BODY.value,
        )


class CheckDataAccountScene(Scene, state=SceneName.DATA.check):
    """Сцена проверки лицевого счёта"""

    @on.callback_query.enter()
    async def handle_enter(self, callback: CallbackQuery) -> None:
        async with async_session() as session:
            user_id = callback.from_user.id
            user_repo = CompositeManager(session)
            user_accounts = await user_repo.get_all_account_by_tg_id(str(user_id))
            account_keys = [_ for _ in user_accounts.values()]
            for key in account_keys:
                if isinstance(key, str):
                    break
                await callback.answer()
                await callback.message.answer(BotMessage.NO_ACCOUNT.value)
            await callback.answer()
            await callback.message.answer(BotMessage.WAIT_REQUEST_DATA.value)

            # TODO: тут будет функция для добавления задачи в Редис для парсера
