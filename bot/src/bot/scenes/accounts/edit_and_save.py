from enum import Enum
from typing import Any

from aiogram import F
from aiogram.enums import ParseMode
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
    """Сцена редактирования аккаунта пользователя.

    Позволяет выбрать, какое поле аккаунта редактировать (код лицевого счёта или телефон)
    в зависимости от типа услуги, а также валидирует введённое пользователем значение.
    """

    def __init_subclass__(cls, state: str = None, **kwargs: Any) -> None:
        """Инициализация подкласса сцены с передачей состояния (state)."""
        super().__init_subclass__(state=state, **kwargs)

    @staticmethod
    def get_utility_type(utility_name: str) -> str:
        """Возвращает тип поля для услуги (например, 'code' или 'phone')
        по её техническому имени.
        """
        return setting.ACCOUNT_TYPE.get(utility_name)

    @on.callback_query.enter()
    async def handle_edit(
            self,
            callback: CallbackQuery,
            state: FSMContext,
    ) -> None:
        """Обрабатывает вход в сцену редактирования аккаунта через callback.

        В зависимости от типа услуги показывает соответствующее сообщение:
        - Запрос на ввод лицевого счёта (если услуга требует code)
        - Запрос на ввод телефона (если услуга требует phone)

        Параметры:
            callback (CallbackQuery): Входящий callback от Telegram.
            state (FSMContext): Контекст текущего состояния FSM.
        """
        current_state = await state.get_state()
        utility_model_name = SceneName.editor_to_utility_name(current_state)
        utility: Enum = SceneName.scene_editor_to_utility_label(current_state)
        utility_type = self.get_utility_type(utility_model_name)
        if utility_type == 'code':
            await callback.message.answer(
                BotMessage.EDIT_ACCOUNT.value.format(utility=utility.value),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif utility_type == 'phone':
            await callback.message.answer(
                BotMessage.EDIT_PHONE.value.format(utility=utility.value),
                parse_mode=ParseMode.MARKDOWN,
            )

    @on.message()
    async def handle_check_account(
            self, message: Message, state: FSMContext,
    ) -> None:
        """Валидирует введённый пользователем номер аккаунта или телефон.

        Если валидация не проходит — сообщает об ошибке
        и предлагает повторить ввод.
        Если всё верно — сообщает об успешном изменении
        и переводит пользователя на следующий этап сцены.

        Параметры:
            message (Message): Входящее сообщение пользователя.
            state (FSMContext): Контекст текущего состояния FSM.
        """
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
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=main_kb(),
            )
            current_state = await state.get_state()
            scene_enum: SceneName = SceneName.editor_to_scene_enum(current_state)
            next_state = scene_enum.save
            await self.wizard.goto(next_state)


class SaveAccountScene(Scene):
    """Сцена сохранения аккаунта пользователя.
    Обрабатывает ввод данных для сохранения лицевого счёта в базу данных,
    меняет статус пользователя после добавления первого аккаунта.
    """

    def __init_subclass__(cls, state: str = None, **kwargs: Any) -> None:
        """Инициализация подкласса сцены с передачей состояния (state)."""
        super().__init_subclass__(state=state, **kwargs)

    @staticmethod
    def mapping_account(current_state):
        """Соотносит сцену с техническим именем услуги (UtilityName)."""
        mapping = {
            SceneName.ELECTRICITY.save: UtilityName.ELECTRICITY.value,
            SceneName.GAS.save: UtilityName.GAS.value,
            SceneName.GAS_SERVICE.save: UtilityName.GAS_SERVICE.value,
            SceneName.WATER.save: UtilityName.WATER.value,
        }
        return mapping.get(current_state)

    @on.message.enter()
    async def handle_enter(self, message: Message, state: FSMContext) -> None:
        """Обрабатывает вход пользователя в сцену сохранения аккаунта.

        Сохраняет новый аккаунт пользователя в базу данных,
        меняет статус пользователя после добавления первого аккаунта,
        отправляет сообщение с предложением выбрать следующее действие.

        Параметры:
            message (Message): Входящее сообщение пользователя.
            state (FSMContext): Контекст текущего состояния FSM.
        """
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
        """Обрабатывает нажатие на inline-кнопку добавления нового аккаунта в сцене.

        Очищает reply_markup, завершает текущий callback
        и переводит пользователя на следующий этап сцены.

        Параметры:
            callback (CallbackQuery): Входящий callback от Telegram.
        """
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
