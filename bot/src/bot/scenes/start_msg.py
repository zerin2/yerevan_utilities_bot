from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

import settings as setting
from bot.crud.status import status_crud
from bot.crud.user import user_crud
from bot.enums.profile_enums import BotMessage
from bot.enums.scene_enums import SceneName
from bot.enums.setting_enums import UserAccountStatus, UserPersonalSettings
from bot.keyboards.accounts import CALLBACK_DATA_ACCOUNT_KEYBOARD, add_accounts
from bot.keyboards.main import display_debt, main_kb, mini_main_kb
from db.core import async_session
from db.models.models import UserProfile


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
            user_id = message.from_user.id
            await user_crud.create_user_if_not_exist(
                session,
                str(user_id),
            )
            await session.flush()

            user: UserProfile = await user_crud.get_user_by_tg_id(
                session,
                user_id,
            )
            user_status_id = user.status_id
            if not user_status_id:
                await user_crud.update_status(
                    session,
                    user_id,
                    setting.PERSONAL_SETTINGS[
                        UserPersonalSettings.ACCOUNT_STATUS.value
                    ],
                )
                await user_crud.update_notice_type(
                    session,
                    user_id,
                    setting.PERSONAL_SETTINGS[
                        UserPersonalSettings.NOTICE_TYPE.value
                    ],
                )
                await user_crud.update_notice_state(
                    session,
                    user_id,
                    setting.PERSONAL_SETTINGS[
                        UserPersonalSettings.NOTICE_STATE.value
                    ],
                )
                await session.commit()

            user_status = await status_crud.get_status_by_id(
                session,
                user_status_id,
            )
            if user_status.name == UserAccountStatus.NEW.value:
                await message.answer(
                    BotMessage.START.value.format(user_name=user_name),
                    parse_mode='Markdown',
                    reply_markup=mini_main_kb(),
                )
                await message.answer(
                    BotMessage.NEW_PERSON.value,
                    reply_markup=add_accounts(),
                )
            else:
                await message.answer(
                    BotMessage.START.value.format(user_name=user_name),
                    parse_mode='Markdown',
                    reply_markup=main_kb(),
                )
                await message.answer(
                    BotMessage.OLD_PERSON.value,
                    reply_markup=display_debt(),
                )

    @on.callback_query(F.data.in_(CALLBACK_DATA_ACCOUNT_KEYBOARD))
    async def handle_add_account(self, callback: CallbackQuery) -> None:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()
        await self.wizard.goto(callback.data)
