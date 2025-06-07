from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message
from enums.profile_enums import BotMessage
from enums.scene_enums import SceneName
from enums.setting_enums import AccountStatus, PersonalSettings

import bot.main.keyboards as kb
import settings as setting
from bot.manager.composite_manager import CompositeManager
from db.core import async_session
from db.models import UsersProfile


class StartMsgScene(Scene, state=SceneName.START_MSG.value):
    """Отправляет приветственное сообщение и подключает основную клавиатуру
    и проверяет, есть ли у пользователя связанные настройки.
    Сохраняет в бд дефолтные настройки.
    """

    @on.message.enter()
    async def handle_enter(self, message: Message) -> None:
        user_name = (
                message.from_user.username
                or message.from_user.first_name
                or 'пользователь'
        )
        async with async_session() as session:
            user_repo = CompositeManager(session)
            user_id = message.from_user.id

            await user_repo.add_user_if_not_exists(str(user_id))
            await session.flush()

            user: UsersProfile = await user_repo.get_user_by_tg_id(user_id)
            if not user.status_id:
                await user_repo.edit_user_status(
                    user_id,
                    setting.PERSONAL_SETTINGS[
                        PersonalSettings.ACCOUNT_STATUS.value
                    ],
                )
                await user_repo.edit_user_notice_type(
                    user_id,
                    setting.PERSONAL_SETTINGS[
                        PersonalSettings.NOTICE_TYPE.value
                    ],
                )
                await user_repo.edit_user_notice_state(
                    user_id,
                    setting.PERSONAL_SETTINGS[
                        PersonalSettings.NOTICE_STATE.value
                    ],
                )
                await session.commit()
            user_status = await user_repo.get_user_status(user_id)

            if user_status.name == AccountStatus.NEW.value:
                await message.answer(
                    BotMessage.START.value.format(user_name=user_name),
                    parse_mode='Markdown',
                    reply_markup=kb.mini_main_kb(),
                )
                await message.answer(
                    BotMessage.NEW_PERSON.value,
                    reply_markup=kb.add_accounts(),
                )
            else:
                await message.answer(
                    BotMessage.START.value.format(user_name=user_name),
                    parse_mode='Markdown',
                    reply_markup=kb.main_kb(),
                )
                await message.answer(
                    BotMessage.OLD_PERSON.value,
                    reply_markup=kb.display_debt(),
                )

    @on.callback_query(F.data.in_(kb.CALLBACK_DATA_ACCOUNT_KEYBOARD))
    async def handle_add_account(self, callback: CallbackQuery) -> None:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()
        await self.wizard.goto(callback.data)
