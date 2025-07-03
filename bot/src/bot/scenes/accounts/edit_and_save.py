from enum import Enum
from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message
from pydantic import ValidationError

import settings as setting
from bot.crud.account import user_account_crud
from bot.crud.user import user_crud
from bot.enums.profile_enums import BotMessage
from bot.enums.scene_enums import SceneName, UtilityName
from bot.keyboards.accounts import (
    CALLBACK_DATA_ACCOUNT_KEYBOARD,
    check_or_add_or_request_account,
)
from bot.keyboards.main import main_kb
from bot.scenes.accounts.schemas import AccountInput
from db.core import async_session


class EditAccountScene(Scene):
    """ """

    def __init_subclass__(cls, state: str = None, **kwargs: Any) -> None:
        super().__init_subclass__(state=state, **kwargs)

    @staticmethod
    def get_utility_type(utility_name: str) -> str:
        """Сопоставляет услугу с типом поля услуги из settings(code | phone)."""
        for key, value in setting.ACCOUNT_TYPE.items():
            if key == utility_name:
                return value
        return None

    @on.callback_query.enter()
    async def handle_edit(
            self, callback:
            CallbackQuery,
            state: FSMContext,
    ) -> None:
        """ """
        current_state = await state.get_state()
        utility_model_name = SceneName.to_utility_name(current_state)
        utility: Enum = SceneName.to_utility_description(current_state)
        if self.get_utility_type(utility_model_name) == 'code':
            await callback.message.answer(
                BotMessage.EDIT_ACCOUNT.value.format(utility=utility.value),
                parse_mode='Markdown',
            )
        elif self.get_utility_type(utility_model_name) == 'phone':
            await callback.message.answer(
                BotMessage.EDIT_PHONE.value.format(utility=utility.value),
                parse_mode='Markdown',
            )

    @on.message()
    async def handle_check_account(
            self, message: Message, state: FSMContext,
    ) -> None:
        """ """
        try:
            account_input = AccountInput(value=message.text)
            cleaned_value = account_input.value
        except ValidationError as e:
            for err in e.errors():
                await message.reply(err['msg'])
            await message.answer(BotMessage.REPEAT_EDIT.value)
        else:
            await message.answer(
                BotMessage.SUCCESS_EDIT.value.format(
                    account_number=cleaned_value,
                ),
                parse_mode='Markdown',
                reply_markup=main_kb(),
            )
            current_state = await state.get_state()
            utility = SceneName.to_save(current_state)
            await self.wizard.goto(utility.save)


class SaveAccountScene(Scene):
    """ """

    def __init_subclass__(cls, state: str = None, **kwargs: Any) -> None:
        super().__init_subclass__(state=state, **kwargs)

    @staticmethod
    def mapping_account(current_state):
        mapping = {
            SceneName.ELECTRICITY.save: UtilityName.ELECTRICITY.value,
            SceneName.GAS.save: UtilityName.GAS.value,
            SceneName.GAS_SERVICE.save: UtilityName.GAS_SERVICE.value,
            SceneName.WATER.save: UtilityName.WATER.value,
        }
        return mapping.get(current_state)

    @on.message.enter()
    async def handle_enter(self, message: Message, state: FSMContext) -> None:
        async with async_session() as session:
            user_id = str(message.from_user.id)
            user_account = message.text.strip()
            utility_name = self.mapping_account(await state.get_state())
            await user_account_crud.create_account(
                session, user_id, user_account, utility_name,
            )
            await user_crud.change_user_status_after_first_add_account(
                session,
                user_id,
            )
            await session.commit()
            await message.answer(
                BotMessage.CHOOSE_NEXT_TASK.value,
                reply_markup=check_or_add_or_request_account(),
            )

    @on.callback_query(F.data.in_(CALLBACK_DATA_ACCOUNT_KEYBOARD))
    async def handle_add_account(self, callback: CallbackQuery) -> None:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()
        await self.wizard.goto(callback.data)
        await callback.message.delete()


class EditElectricityAccountScene(
    EditAccountScene,
    state=SceneName.ELECTRICITY.editor,
):
    """Добавления счёта(электричество)."""


class SaveElectricityAccountScene(
    SaveAccountScene,
    state=SceneName.ELECTRICITY.save,
):
    """Сохранение счета(электричество)."""


class EditGasAccountScene(
    EditAccountScene,
    state=SceneName.GAS.editor,
):
    """Добавления счёта(газ)."""


class SaveGasAccountScene(
    SaveAccountScene,
    state=SceneName.GAS.save,
):
    """Сохранение счета(газ)."""


class EditGasServiceAccountScene(
    EditAccountScene,
    state=SceneName.GAS_SERVICE.editor,
):
    """Сцена управления счётом обслуживания газа."""


class SaveGasServiceAccountScene(
    SaveAccountScene,
    state=SceneName.GAS_SERVICE.save,
):
    """Сохранение счета(обслуживания газа)."""


class EditWaterAccountScene(
    EditAccountScene,
    state=SceneName.WATER.editor,
):
    """Добавления счёта(обслуживания воды)."""


class SaveWaterAccountScene(
    SaveAccountScene,
    state=SceneName.WATER.save,
):
    """Сохранение счета(обслуживания воды)."""
