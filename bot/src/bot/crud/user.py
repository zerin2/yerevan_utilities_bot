from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.core.exceptions import EndNoticeInterval404, StartNoticeInterval404
from bot.core.handle_errors import handle_db_errors
from bot.crud.base import CRUDBase
from bot.crud.notice import (
    end_notice_interval_crud,
    notice_type_crud,
    start_notice_interval_crud,
)
from bot.crud.status import status_crud
from bot.enums.notice_enums import NoticeFlag
from bot.enums.setting_enums import Status, UserPersonalSettings
from db.models.models import StatusType, UserProfile
from logs.config import bot_logger
from settings import DEFAULT_PERSONAL_SETTINGS


class CRUDUser(CRUDBase):
    async def get_user_by_tg_id(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> UserProfile | None:
        """Получение 'user' по 'telegram_id'."""
        return await self.get_by_field(
            session,
            'telegram_id',
            str(telegram_id),
        )

    async def remove_user_by_tg_id(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> None:
        """Удаление 'user' по 'telegram_id'."""
        user_profile: UserProfile = await self.get_by_field(
            session,
            'telegram_id',
            str(telegram_id),
        )
        if user_profile:
            await self.remove_by_id(session, user_profile.id)

    async def create_user(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> UserProfile:
        """Создание нового user с telegram_id."""
        notice_type = await notice_type_crud.get_or_create_notice_type(
            session,
            DEFAULT_PERSONAL_SETTINGS.get(
                UserPersonalSettings.NOTICE_TYPE.value,
            ),
        )
        return await self.create(session, {
            'telegram_id': str(telegram_id),
            'is_delivery_blocked': DEFAULT_PERSONAL_SETTINGS.get(
                UserPersonalSettings.IS_DELIVERY_BLOCKED.value,
            ),
            'notice_state': DEFAULT_PERSONAL_SETTINGS.get(
                UserPersonalSettings.NOTICE_STATE.value,
            ),
            'notice_type_id': notice_type.id,
        })

    async def get_or_create_user(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> UserProfile:
        """Получение или создание нового user по telegram_id."""
        user = await self.get_user_by_tg_id(session, str(telegram_id))
        if not user:
            return await self.create_user(session, str(telegram_id))
        return user

    async def update_status(
            self,
            session: AsyncSession,
            telegram_id: str,
            status: str,
    ) -> UserProfile:
        """Обновляет статус пользователя."""
        user = await self.get_user_by_tg_id(session, telegram_id)
        if not user:
            raise ValueError('Пользователь не найден')
        status_obj = await status_crud.get_status_by_name(session, status)
        if not status_obj:
            status_obj = await status_crud.create_status(session, status)
        user.status_id = status_obj.id
        await session.flush()
        return user

    async def update_notice_type(
            self,
            session: AsyncSession,
            telegram_id: str,
            notice_type_value: str,
    ) -> UserProfile:
        """Обновляет тип оповещения пользователя."""
        user = await self.get_user_by_tg_id(session, telegram_id)
        if not user:
            raise ValueError('Пользователь не найден')
        notice_type = await notice_type_crud.get_notice_type_by_name(
            session, notice_type_value,
        )
        if not notice_type:
            notice_type = await notice_type_crud.create_notice_type(
                session, notice_type_value,
            )
        user.notice_type_id = notice_type.id
        await session.flush()
        return user

    async def update_notice_state(
            self,
            session: AsyncSession,
            telegram_id: str,
            notice_state: str,
    ) -> UserProfile:
        """Обновляет состояние оповещения пользователя."""
        user = await self.get_user_by_tg_id(session, telegram_id)
        if not user:
            raise ValueError('Пользователь не найден')
        user.notice_state = (str(notice_state))
        await session.flush()
        return user

    async def get_user_status(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> StatusType:
        """Получает статус пользователя."""
        user: UserProfile = await self.get_user_by_tg_id(session, telegram_id)
        if not user:
            raise ValueError('Пользователь не найден')
        user_status: StatusType = await status_crud.get_status_by_id(
            session, user.status_id,
        )
        return user_status

    async def change_user_status_after_first_add_account(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> UserProfile | None:
        """Изменяет статус пользователя после добавления первого счета."""
        user: UserProfile = await self.get_user_by_tg_id(session, telegram_id)
        user_status_obj = status_crud.get_status_by_id(session, user.status_id)
        if user_status_obj and user_status_obj.name == Status.NEW.value:
            return await self.update_status(
                session,
                telegram_id,
                Status.ACTIVE.value,
            )
        return None

    @handle_db_errors
    async def get_start_notice_interval(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> Optional[UserProfile]:
        query = select(
            self.model,
        ).options(
            selectinload(self.model.start_notice_interval),
        ).where(self.model.telegram_id == telegram_id)
        result_query = await session.execute(query)
        user: UserProfile = result_query.scalar_one_or_none()
        start_notice_interval = user.start_notice_interval
        if not start_notice_interval:
            msg = (
                'StartNoticeInterval404: '
                'Не найден начальный интервал оповещения'
            )
            bot_logger.error(msg)
            raise StartNoticeInterval404(msg)
        return start_notice_interval

    @handle_db_errors
    async def get_end_notice_interval(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> Optional[UserProfile]:
        query = select(
            self.model,
        ).options(
            selectinload(self.model.end_notice_interval),
        ).where(self.model.telegram_id == telegram_id)
        result_query = await session.execute(query)
        user: UserProfile = result_query.scalar_one_or_none()
        end_notice_interval = user.end_notice_interval
        if not end_notice_interval:
            msg = (
                'EndNoticeInterval404: '
                'Не найден конечный интервал оповещения'
            )
            bot_logger.error(msg)
            raise EndNoticeInterval404(msg)
        return end_notice_interval

    @handle_db_errors
    async def get_user_all_notice_info(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> dict:
        """Возвращает всю информацию об оповещениях пользователя."""
        query = select(self.model).options(
            selectinload(self.model.notice_type),
            selectinload(self.model.start_notice_interval),
            selectinload(self.model.end_notice_interval),
        ).where(self.model.telegram_id == str(telegram_id))
        result = await session.execute(query)
        user: UserProfile = result.scalar_one_or_none()
        return dict(
            notice_state=user.notice_state,
            notice_type=(
                user.notice_type.name
                if user.notice_type else None
            ),
            start_notice_interval=(
                user.start_notice_interval.name
                if user.start_notice_interval else None
            ),
            end_notice_interval=(
                user.end_notice_interval.name
                if user.end_notice_interval else None
            ),
        )

    async def update_notice_interval(
            self,
            session: AsyncSession,
            telegram_id: str,
            value: str,
            flag: NoticeFlag,
    ) -> UserProfile:
        """Обновляет start или end notice interval для пользователя."""
        if flag == NoticeFlag.START.value:
            notice_crud = start_notice_interval_crud
            attr_name = 'start_notice_interval_id'
        elif flag == NoticeFlag.END.value:
            notice_crud = end_notice_interval_crud
            attr_name = 'end_notice_interval_id'
        else:
            raise ValueError('Некорректный флаг notice interval')
        user: UserProfile = await self.get_user_by_tg_id(
            session, telegram_id,
        )
        if not user:
            raise ValueError('Пользователь не найден')
        notice_interval = await notice_crud.get_interval_by_name(
            session, value,
        )
        if not notice_interval:
            notice_interval = await notice_crud.create_interval(
                session, value,
            )
            await session.flush()
        setattr(user, attr_name, notice_interval.id)
        await session.flush()
        return user


user_crud = CRUDUser(UserProfile)
