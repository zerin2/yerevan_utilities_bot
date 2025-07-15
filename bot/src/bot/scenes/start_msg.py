from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from bot.crud.account import user_account_crud
from bot.crud.user import user_crud
from bot.enums.profile_enums import BotMessage
from bot.enums.scene_enums import SceneName
from bot.enums.setting_enums import Status, UserPersonalSettings
from bot.keyboards.accounts import CALLBACK_DATA_ACCOUNT_KEYBOARD, add_accounts
from bot.keyboards.main import display_debt, main_kb, mini_main_kb
from db.core import async_session
from db.models.models import StatusType, UserProfile, UserAccount
from settings import DEFAULT_PERSONAL_SETTINGS


class StartMsgScene(Scene, state=SceneName.START_MSG.value):
    """Отправляет приветственное сообщение и подключает основную клавиатуру
    и проверяет, есть ли у пользователя связанные настройки.
    Создает для новых пользователей дефолтные счета и настройки.
    """

    @on.message.enter()
    async def handle_enter(self, message: Message) -> None:
        user_name = (
                message.from_user.username
                or message.from_user.first_name
                or 'пользователь'
        )
        async with async_session() as session:
            user_telegram_id = message.from_user.id
            user_obj: UserProfile = await user_crud.get_or_create_user(
                session,
                str(user_telegram_id),
            )
            await session.flush()
            user_accounts: UserAccount = await user_account_crud.get_all_accounts(
                session,
                str(user_telegram_id),
            )
            if not user_accounts:
                await user_account_crud.create_default_accounts(
                    session,
                    user_obj.id,
                )
            user_status_id = user_obj.status_id
            if not user_status_id:
                await user_crud.update_status(
                    session,
                    user_telegram_id,
                    DEFAULT_PERSONAL_SETTINGS.get(
                        UserPersonalSettings.STATUS.value,
                    ),
                )
                await user_crud.update_notice_state(
                    session,
                    user_telegram_id,
                    DEFAULT_PERSONAL_SETTINGS.get(
                        UserPersonalSettings.NOTICE_STATE.value,
                    ),
                )
                await user_crud.update_notice_type(
                    session,
                    user_telegram_id,
                    DEFAULT_PERSONAL_SETTINGS.get(
                        UserPersonalSettings.NOTICE_TYPE.value,
                    ),
                )
                await session.commit()

            user_status: StatusType = await user_crud.get_user_status(
                session,
                str(user_telegram_id),
            )
            if user_status.name == Status.NEW.value:
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
