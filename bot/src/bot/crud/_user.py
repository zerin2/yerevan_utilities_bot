
from bot.crud._base import BaseBotManager


class UserBotManager(BaseBotManager):
    """Управление действиями, связанными с пользователями в бд:
    добавление, получение информации о пользователе и
    запись истории взаимодействия пользователя с ботом.
    """

    # async def get_user_by_tg_id(self, tg_id: str) -> UsersProfile | None:
    #     """Получение 'user' из бд по 'user_tg_id'."""
    #     return await self.get_by_field(
    #         self.USER_PROFILE_MODEL, 'telegram_id', str(tg_id),
    #     )

    # @handle_db_errors
    # async def del_user_by_id(self, tg_id: str) -> None:
    #     """Удаление 'user' из бд по 'user_tg_id'."""
    #     return await self.delete_instance(
    #         self.USER_PROFILE_MODEL, 'telegram_id', str(tg_id),
    #     )
    #
    # async def is_exist_user(self, tg_id: str) -> bool | None:
    #     """Проверка, существует ли пользователь с указанным 'tg_id'."""
    #     return await self.is_exist(
    #         self.USER_PROFILE_MODEL, 'telegram_id', str(tg_id),
    #     )
    #
    # @handle_db_errors
    # async def add_user(self, tg_id: str) -> UsersProfile | None:
    #     """Добавьте нового пользователя с 'user_tg_id',
    #     если пользователь не существует.
    #     """
    #     return await self.add_new_instance(
    #         self.USER_PROFILE_MODEL, {'telegram_id': str(tg_id)},
    #     )
    #
    # @handle_db_errors
    # async def add_user_if_not_exists(self, tg_id: str) -> UsersProfile | None:
    #     """Проверяет, существует ли пользователь с заданным Telegram ID.
    #     Если пользователь не существует в базе данных, создаёт нового пользователя.
    #     """
    #     if not await self.is_exist_user(str(tg_id)):
    #         return await self.add_user(str(tg_id))
    #     return None

    # @handle_db_errors
    # async def get_or_create_user(self, tg_id: str) -> UsersProfile:
    #     """Получает пользователя по его Telegram ID,
    #     если такой пользователь существует.
    #     Если пользователь не найден,
    #     создаёт нового пользователя с указанным Telegram ID
    #     и возвращает его.
    #     """
    #     user = await self.get_user_by_tg_id(str(tg_id))
    #     if user:
    #         return user
    #     await self.add_user(str(tg_id))
    #     user = await self.get_user_by_tg_id(str(tg_id))
    #     return user

    # @handle_db_errors
    # async def write_history(
    #         self, message: Message, state: FSMContext | str = '',
    # ) -> UsersHistory | None:
    #     """Запись информации о сообщениях пользователей в бд,
    #     сохраняя историю взаимодействий с ботом.
    #     Проверяет, существует ли пользователь в базе данных,
    #     и добавляет его, если его нет.
    #     """
    #     user_id = message.from_user.id
    #     chat_id = message.chat.id
    #     message_id = message.message_id
    #     message_content = message.text
    #
    #     if isinstance(state, FSMContext):
    #         state = str(await state.get_data())
    #
    #     user = await self.get_or_create_user(user_id)
    #
    #     if not user:
    #         raise ValueError(
    #             'Передано пустое значение в \'user\'.',
    #         )
    #     user_instance = await self.add_new_instance(
    #         self.USER_HISTORY_MODEL,
    #         {
    #             'user_id': user.id,
    #             'chat_id': chat_id,
    #             'message_id': message_id,
    #             'message_content': message_content,
    #             'state': state,
    #         },
    #     )
    #     return user_instance

    # async def get_start_notice_interval(
    #         self,
    #         tg_id: str,
    # ) -> StartNoticeInterval | None:
    #     """Возвращает начальный интервал оповещения.
    #     """
    #     model = self.USER_PROFILE_MODEL
    #     query = select(
    #         model,
    #     ).options(
    #         selectinload(model.start_notice_interval),
    #     ).where(model.telegram_id == str(tg_id))
    #     result = await self.session.execute(query)
    #     user: UsersProfile = result.scalar_one_or_none()
    #     start_notice_interval = user.start_notice_interval
    #     if not start_notice_interval:
    #         msg = 'Не найден начальный интервал оповещения'
    #         bot_logger.exception(msg)
    #         raise UserBotManager.StartNoticeInterval404(msg)
    #     return start_notice_interval
    #
    # async def get_end_notice_interval(
    #         self,
    #         tg_id: str,
    # ) -> EndNoticeInterval | None:
    #     """Возвращает конечный интервал оповещения.
    #     """
    #     model = self.USER_PROFILE_MODEL
    #     query = select(
    #         model,
    #     ).options(
    #         selectinload(model.end_notice_interval),
    #     ).where(model.telegram_id == str(tg_id))
    #     result = await self.session.execute(query)
    #     user: UsersProfile = result.scalar_one_or_none()
    #     end_notice_interval = user.end_notice_interval
    #     if not end_notice_interval:
    #         msg = 'Не найден конечный интервал оповещения'
    #         bot_logger.exception(msg)
    #         raise UserBotManager.EndNoticeInterval404(msg)
    #     return end_notice_interval

    # async def get_user_status(self, tg_id: str) -> StatusType | None:
    #     """Возвращает статуса пользователя.
    #     """
    #     user: UsersProfile = await self.get_by_field(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         variable=str(tg_id),
    #     )
    #     if not user or user.status_id is None:
    #         return None
    #     return await self.get_by_field(
    #         model=self.STATUS_TYPE_MODEL,
    #         field_name='id',
    #         variable=user.status_id,
    #     )

    # async def get_user_notice_type(self, tg_id: str) -> NoticeType | None:
    #     """Возвращает тип оповещения пользователя.
    #     """
    #     user: UsersProfile = await self.get_by_field(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         variable=str(tg_id),
    #     )
    #     user_notice_type = user.notice_type
    #     if not user_notice_type:
    #         msg = 'Не найден тип оповещения'
    #         bot_logger.exception(msg)
    #         raise UserBotManager.NoticeType404(msg)
    #     return user_notice_type

    # async def get_user_all_notice_info(self, tg_id: str) -> dict:
    #     """Возвращает всю информацию об оповещениях пользователя."""
    #     model = self.USER_PROFILE_MODEL
    #     query = select(model).options(
    #         selectinload(model.notice_type),
    #         selectinload(model.start_notice_interval),
    #         selectinload(model.end_notice_interval),
    #     ).where(model.telegram_id == str(tg_id))
    #
    #     result = await self.session.execute(query)
    #     user: UsersProfile = result.scalar_one_or_none()
    #     return {
    #         'notice_state': user.notice_state,
    #         'notice_type': (user.notice_type.name
    #                         if user.notice_type else None),
    #         'start_notice_interval': (user.start_notice_interval.name
    #                                   if user.start_notice_interval else None),
    #         'end_notice_interval': (user.end_notice_interval.name
    #                                 if user.end_notice_interval else None),
    #     }

    # async def edit_user_status(self,
    #                            tg_id: str,
    #                            status: str) -> UsersProfile:
    #     """Обновляет статус пользователя в базе данных.
    #     Параметры:
    #     ----------
    #     tg_id : str
    #         Telegram ID пользователя.
    #     status : str
    #         Новый статус пользователя.
    #     Возвращает:
    #     ----------
    #     UsersProfile | None
    #     Обновленный профиль пользователя или None,
    #     если не удалось изменить статус.
    #     """
    #     status_instance = await self.get_by_field(
    #         model=self.STATUS_TYPE_MODEL,
    #         field_name='name',
    #         variable=status,
    #     )
    #     if not status_instance:
    #         status_instance = await self.add_new_instance(
    #             model=self.STATUS_TYPE_MODEL,
    #             fields={'name': status},
    #         )
    #         await self.session.flush()
    #     updated_user = await self.edit_one_value(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         value=str(tg_id),
    #         update_field_name='status_id',
    #         new_value=status_instance.id,
    #     )
    #     return updated_user

    # async def edit_user_notice_type(
    #         self,
    #         tg_id: str,
    #         notice: str,
    # ) -> UsersProfile:
    #     """Обновляет тип оповещения пользователя в базе данных.
    #     Параметры:
    #     ----------
    #     tg_id : str
    #         Telegram ID пользователя.
    #     notice : str
    #         Новый вид оповещения.
    #     Возвращает:
    #     ----------
    #     UsersProfile | None
    #     Обновленный профиль пользователя или None,
    #     если не удалось изменить тип оповещения.
    #     """
    #     notice_instance = await self.get_by_field(
    #         model=self.NOTICE_TYPE_MODEL,
    #         field_name='name',
    #         variable=notice,
    #     )
    #     if not notice_instance:
    #         notice_instance = await self.add_new_instance(
    #             model=self.NOTICE_TYPE_MODEL,
    #             fields={'name': notice},
    #         )
    #         await self.session.flush()
    #     updated_user = await self.edit_one_value(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         value=str(tg_id),
    #         update_field_name='notice_type_id',
    #         new_value=notice_instance.id,
    #     )
    #     return updated_user

    # async def edit_user_notice_state(
    #         self,
    #         tg_id: str,
    #         state: str,
    # ) -> UsersProfile:
    #     """
    #
    #     """
    #     return await self.edit_one_value(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         value=str(tg_id),
    #         update_field_name='notice_state',
    #         new_value=str(state),
    #     )

    # async def edit_user_start_notice_hour(
    #         self,
    #         tg_id: str,
    #         value: str,
    # ) -> UsersProfile:
    #     """
    #
    #     """
    #     model = self.START_NOTICE_INTERVAL_MODEL
    #     notice_hour_instance = await self.get_by_field(
    #         model=model,
    #         field_name='name',
    #         variable=value,
    #     )
    #     if not notice_hour_instance:
    #         notice_hour_instance = await self.add_new_instance(
    #             model=model,
    #             fields={'name': value},
    #         )
    #         await self.session.flush()
    #
    #     return await self.edit_one_value(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         value=str(tg_id),
    #         update_field_name='start_notice_interval_id',
    #         new_value=notice_hour_instance.id,
    #     )
    #
    # async def edit_user_end_notice_hour(
    #         self,
    #         tg_id: str,
    #         value: str,
    # ) -> UsersProfile:
    #     """
    #
    #     """
    #     model = self.END_NOTICE_INTERVAL_MODEL
    #     notice_hour_instance = await self.get_by_field(
    #         model=model,
    #         field_name='name',
    #         variable=value,
    #     )
    #     if not notice_hour_instance:
    #         notice_hour_instance = await self.add_new_instance(
    #             model=model,
    #             fields={'name': value},
    #         )
    #         await self.session.flush()
    #     return await self.edit_one_value(
    #         model=self.USER_PROFILE_MODEL,
    #         field_name='telegram_id',
    #         value=str(tg_id),
    #         update_field_name='end_notice_interval_id',
    #         new_value=notice_hour_instance.id,
    #     )

    # async def change_user_status_after_first_add_account(
    #         self,
    #         user_id: str,
    # ) -> UsersProfile | None:
    #     """Изменяет статус пользователя после добавления первого счета."""
    #     current_status: StatusType | None = await self.get_user_status(user_id)
    #     if current_status and current_status.name == AccountStatus.NEW.value:
    #         return await self.edit_user_status(
    #             user_id,
    #             AccountStatus.ACTIVE.value,
    #         )
    #     return None
