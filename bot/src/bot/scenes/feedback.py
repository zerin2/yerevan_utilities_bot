from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message
from enums.profile_enums import BotMessage
from enums.scene_enums import FeedbackType, SceneName

import bot.main.keyboards as kb
import bot.main.utils as tool
from bot.manager.composite_manager import CompositeManager
from db.core import async_session


class FeedbackScene(Scene, state=SceneName.FEEDBACK.display):
    """Сцена обратной связи."""

    @on.message.enter()
    async def handle_enter(self, message: Message) -> None:
        await message.answer(BotMessage.FEEDBACK.value)
        await message.answer(
            BotMessage.FEEDBACK_ADDITIONAL.value,
            reply_markup=kb.feedback_additional(),
        )

    @on.callback_query()
    async def handle_account_selection(self, callback: CallbackQuery) -> None:
        await callback.answer()
        await self.wizard.goto(callback.data)
        await callback.message.delete()


class FeedbackReviewScene(Scene, state=SceneName.USUAL_REVIEW.editor):
    """Сцена для обработки отзывов в боте.
    Описание:
    ----------
    Эта сцена позволяет пользователям оставлять отзывы о работе бота.
    Она принимает текстовые сообщения, валидирует их и сохраняет в базу данных.
    Методы:
    -------
    handle_enter(callback: CallbackQuery) -> None
        Обрабатывает вход в сцену и отправляет пользователю приветственное сообщение.
    handle_msg(message: Message) -> None
        Обрабатывает текстовые сообщения от пользователей.
        - Проверяет текст на валидность (длина, безопасность).
        - Сохраняет валидные сообщения в базе данных.
        - Отправляет пользователю уведомление об успехе или запрос повторить ввод.
    """

    @on.callback_query.enter()
    async def handle_enter(self, callback: CallbackQuery) -> None:
        await callback.message.answer(BotMessage.FEEDBACK_REVIEW.value)

    @on.message()
    async def handle_msg(self, message: Message) -> None:
        """Обрабатывает текстовые сообщения в сцене.
        Параметры:
        ----------
        message : Message
            Объект Message от Telegram.
        Описание:
        ---------
        1. Валидирует текст сообщения с использованием ValidateText.
        2. Если сообщение валидно:
           - Сохраняет отзыв в базе данных через CompositeManager.
           - Отправляет пользователю сообщение об успешной обработке.
        3. Если сообщение невалидно:
           - Уведомляет пользователя о необходимости повторного ввода.
        """
        validator = tool.ValidateText(message)
        validate_message = await validator.validate()

        if validate_message:
            async with async_session() as session:
                feedback_repo = CompositeManager(session)
                await feedback_repo.save_feedback(
                    tg_id=message.from_user.id,
                    feedback_type=FeedbackType.REVIEW.value,
                    feedback_text=validate_message,
                )
                await session.commit()
            await message.reply(BotMessage.FEEDBACK_SUCCESS.value)
        else:
            await message.answer(BotMessage.REPEAT_EDIT.value)


class FoundErrorScene(Scene, state=SceneName.FOUND_ERROR.editor):
    """Сцена для обработки сообщений об ошибках в работе бота.
    Описание:
    ----------
    Эта сцена позволяет пользователям сообщать об ошибках, найденных в боте.
    Сообщения проверяются, валидируются и сохраняются в базе данных.
    Методы:
    -------
    handle_enter(callback: CallbackQuery) -> None
        Обрабатывает вход в сцену и отправляет пользователю приветственное сообщение.
    handle_msg(message: Message) -> None
        Обрабатывает текстовые сообщения от пользователей.
        - Проверяет текст на валидность (длина, безопасность).
        - Сохраняет валидные сообщения об ошибках в базе данных.
        - Отправляет пользователю уведомление об успехе или запрос повторить ввод.
    """

    @on.callback_query.enter()
    async def handle_enter(self, callback: CallbackQuery) -> None:
        await callback.message.answer(BotMessage.FEEDBACK_ERROR.value)

    @on.message()
    async def handle_msg(self, message: Message) -> None:
        """Обрабатывает текстовые сообщения в сцене.
        Параметры:
        ----------
        message : Message
            Объект Message от Telegram.
        Описание:
        ---------
        1. Валидирует текст сообщения с использованием ValidateText.
        2. Если сообщение валидно:
           - Сохраняет описание ошибки в базе данных через CompositeManager.
           - Отправляет пользователю сообщение об успешной обработке.
        3. Если сообщение невалидно:
           - Уведомляет пользователя о необходимости повторного ввода.
        Исключения:
        -----------
        Может генерировать исключения, связанные с базой данных, если сохранение не удалось.
        """
        validator = tool.ValidateText(message)
        validate_message = await validator.validate()

        if validate_message:
            async with async_session() as session:
                feedback_repo = CompositeManager(session)
                await feedback_repo.save_feedback(
                    tg_id=message.from_user.id,
                    feedback_type=FeedbackType.ERROR.value,
                    feedback_text=validate_message,
                )
                await session.commit()
            await message.reply(BotMessage.FEEDBACK_SUCCESS.value)
        else:
            await message.answer(BotMessage.REPEAT_EDIT.value)
