from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.crud.notice import notice_type_crud
from bot.crud.status import status_crud
from bot.enums.setting_enums import UserAccountStatus
from db.models.models import UserProfile, StatusType


class CRUDUser(CRUDBase):
    async def get_user_by_tg_id(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> UserProfile | None:
        """Получение 'user' по 'telegram_id'."""
        return await self.get_by_field(session, 'telegram_id', str(telegram_id))

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
        return await self.create(session, {'telegram_id': str(telegram_id)})

    async def create_user_if_not_exist(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> UserProfile:
        """Создание нового user с telegram_id."""
        user = await self.get_user_by_tg_id(session, str(telegram_id))
        if not user:
            return self.create_user(session, str(telegram_id))
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
            session,
            notice_type_value,
        )
        if not notice_type:
            notice_type = await notice_type_crud.create_notice_type(
                session,
                notice_type_value,
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

    async def change_user_status_after_first_add_account(
            self,
            session: AsyncSession,
            user_id: str,
    ) -> UserProfile | None:
        """Изменяет статус пользователя после добавления первого счета."""
        user: UserProfile = await self.get_user_by_tg_id(session, user_id)
        user_status_obj = status_crud.get_status_by_id(session, user.status_id)
        if user_status_obj and user_status_obj.name == UserAccountStatus.NEW.value:
            return await self.update_status(
                session,
                user_id,
                UserAccountStatus.ACTIVE.value,
            )
        return None


user_crud = CRUDUser(UserProfile)
