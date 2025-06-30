from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from bot.enums.notice_enums import NoticeInterval, NoticeState, NoticeType, NoticeFlag
from bot.enums.profile_enums import BotMessage
from bot.enums.scene_enums import SceneName
from bot.keyboards.settings import change_setting_interval_notice, display_notice_type, \
    display_notice_hours, display_notice_state
from db.core import async_session
from logs.config import bot_logger


class SettingScene(Scene, state=SceneName.SETTING.display):
    """Сцена управления основными настройками пользователя.
    State:
        SceneName.SETTING.display: Состояние,
        в котором отображаются текущие настройки пользователя.
    """

    @on.message.enter()
    async def handle_enter(self, message: Message) -> None:
        """

        """
        async with async_session() as session:
            setting_repo = CompositeManager(session)
            user_id = message.from_user.id
            notice_info: dict = await setting_repo.get_user_all_notice_info(user_id)
            notice_type = notice_info.get('notice_type', BotMessage.UNKNOWN_NOTICE_TYPE.value)
            notice_state = notice_info.get('notice_state', BotMessage.UNKNOWN_NOTICE_STATE.value)
            if notice_type == NoticeType.PERIOD.value:
                start_hour = notice_info.get('start_notice_interval', 'error')
                end_hour = notice_info.get('end_notice_interval', 'error')
                await message.answer(
                    BotMessage.PERSONAL_SETTING_NOTICE_PERIOD.value.format(
                        notice_state=NoticeState.to_human(notice_state),
                        notice_type=NoticeType.to_human(notice_type),
                        start_period=NoticeInterval.to_human(start_hour),
                        end_period=NoticeInterval.to_human(end_hour),
                    ),
                    parse_mode='Markdown',
                    reply_markup=change_setting_interval_notice(),
                )
            else:
                await message.answer(
                    BotMessage.PERSONAL_SETTING_NOTICE_ALL.value.format(
                        notice_state=NoticeState.to_human(notice_state),
                        notice_type=NoticeType.to_human(notice_type),
                    ),
                    parse_mode='Markdown',
                    reply_markup=change_setting_interval_notice(),
                )

    @on.callback_query(F.data == SceneName.NOTICE_INTERVAL.editor)
    @on.callback_query(F.data == SceneName.NOTICE_STATE.editor)
    async def handle_account_selection(self, callback: CallbackQuery) -> None:
        """Обрабатывает выбор пользователя для изменения конкретной настройки.
        Переключает сцену в зависимости от выбора пользователя.

        Args:
            callback (CallbackQuery): Запрос пользователя с выбором.
        Transitions:
            Переход на сцену изменения интервала оповещений
            или состояния оповещений.

        """
        await callback.answer()
        await self.wizard.goto(callback.data)
        await callback.message.delete()


class EditNoticeStateScene(Scene, state=SceneName.NOTICE_STATE.editor):
    """ """

    @on.callback_query.enter()
    async def handle_enter(self, callback: CallbackQuery) -> None:
        """
        """
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            BotMessage.CHOOSE_NOTICE_STATE.value,
            reply_markup=display_notice_state(),
        )

    @on.callback_query()
    async def handle_change_user_notice_state(self, callback: CallbackQuery) -> None:
        """
        """
        await callback.answer()
        try:
            async with async_session() as session:
                user_repo = CompositeManager(session)
                await user_repo.edit_user_notice_state(
                    str(callback.from_user.id), str(callback.data),
                )
                await session.commit()
        except Exception as e:
            e_cls = e.__class__.__name__
            bot_logger.error(f'{e_cls} Ошибка при изменении состояния оповещения: {e}')
            await callback.message.answer(
                f'{e_cls} Произошла ошибка при обновлении ваших настроек. Попробуйте позже.',
            )
            return
        else:
            await callback.message.delete()
            await callback.message.answer(
                BotMessage.SUCCESS_EDIT_SETTINGS.value,
            )


class EditNoticeIntervalScene(Scene, state=SceneName.NOTICE_INTERVAL.editor):
    """ """

    @on.callback_query.enter()
    async def handle_enter(self, callback: CallbackQuery) -> None:
        """
        """
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            BotMessage.CHOOSE_NOTICE_TYPE.value,
            reply_markup=display_notice_type(),
        )

    @on.callback_query()
    async def handle_change_user_notice_interval(self, callback: CallbackQuery) -> None:
        """

        """
        await callback.message.delete()
        new_notice_interval = callback.data
        if new_notice_interval == NoticeType.PERIOD.value:
            await callback.answer()
            await self.wizard.goto(new_notice_interval)
        else:
            try:
                async with async_session() as session:
                    setting_repo = CompositeManager(session)
                    await setting_repo.edit_user_notice_type(
                        str(callback.from_user.id), new_notice_interval,
                    )
                    await session.commit()
            except Exception as e:
                e_cls = e.__class__.__name__
                bot_logger.error(f'{e_cls} Ошибка при изменении типа оповещения: {e}')
                await callback.message.answer(
                    f'Произошла ошибка при обновлении ваших настроек: {e_cls}\n'
                    f'Попробуйте позже.',
                )
                return
            else:
                await callback.message.answer(
                    BotMessage.SUCCESS_EDIT_SETTINGS.value,
                )


class EditPeriodNoticeInterval(Scene, state=NoticeType.PERIOD.value):
    """

    """

    @on.callback_query.enter()
    async def handle_enter(self, callback: CallbackQuery) -> None:
        """
        """
        await callback.message.answer(
            'Выберите начало периода: ',
            reply_markup=display_notice_hours(
                rows=4,
                                                 flag=NoticeFlag.START.value,
            ),
        )

    @on.callback_query(
        F.data.in_([interval.name + kb.start_flag() for interval in NoticeInterval])  # noqa
    )
    async def handle_save_start_notice_interval(self, callback: CallbackQuery) -> None:
        """
        """
        user_id = str(callback.from_user.id)
        user_data = str(callback.data).split('_')[1]
        try:
            async with async_session() as session:
                user_repo = CompositeManager(session)
                await user_repo.edit_user_notice_type(user_id, NoticeType.PERIOD.value)
                await user_repo.edit_user_start_notice_hour(user_id, user_data)
                await session.commit()
        except Exception as e:
            bot_logger.error(
                f'{e.__class__.__name__}, user({user_id}, data({user_data})  '
                f'Ошибка при изменении оповещения: {e}',
            )
            await callback.message.answer(
                'Произошла ошибка при обновлении ваших настроек. '
                'Попробуйте позже.',
            )
            return
        else:
            await callback.answer()
            await callback.message.delete()
            await callback.message.answer(
                'Выберите конец периода: ',
                reply_markup=display_notice_hours(
                    rows=4,
                                                     flag=NoticeFlag.END.value,
                ),
            )

    @on.callback_query(
        F.data.in_([interval.name + kb.end_flag() for interval in NoticeInterval])  # noqa
    )
    async def handle_save_end_notice_interval(self, callback: CallbackQuery) -> None:
        """
        """
        user_id = str(callback.from_user.id)
        user_data = str(callback.data).split('_')[1]
        try:
            async with async_session() as session:
                user_repo = CompositeManager(session)
                await user_repo.edit_user_end_notice_hour(user_id, user_data)
                await session.commit()
        except Exception as e:
            bot_logger.error(
                f'{e.__class__.__name__}, user({user_id}, data({user_data})  '
                f'Ошибка при изменении оповещения: {e}',
            )
            await callback.message.answer(
                'Произошла ошибка при обновлении ваших настроек. '
                'Попробуйте позже.',
            )
            return
        else:
            await callback.answer()
            await callback.message.delete()
            await callback.message.answer(
                BotMessage.SUCCESS_EDIT_SETTINGS.value,
            )
