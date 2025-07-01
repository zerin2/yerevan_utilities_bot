from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.crud.user import user_crud
from bot.crud.utility import utility_crud
from bot.enums.utility_enums import UtilityName
from db.models.models import UserAccount, UserProfile, UtilityType


class CRUDUserAccount(CRUDBase):
    async def create_account(
            self,
            session: AsyncSession,
            telegram_id: str,
            account: str,
            utility_type: UtilityName,
            account_info: str = None,
            city_id: int = None,
            address: str = None,
            traffic: str = None,
            credit: Decimal = None,
            debit: Decimal = None,
            status_id: int = None,
    ) -> UserAccount:
        pass

    async def get_account(
            self,
            session: AsyncSession,
            telegram_id: str,
            utility: UtilityName,
    ) -> Optional[UserAccount]:
        """Получение счета пользователя по utility_name и telegram_id."""
        user: UserProfile = await user_crud.get_user_by_tg_id(
            session, telegram_id
        )
        utility_obj: UtilityType = await utility_crud.get_utility_by_name(
            session, utility
        )
        if not user or not utility_obj:
            return None
        user_id_field = getattr(self.model, 'user_id')
        utility_type_id_field = getattr(self.model, 'utility_type_id')
        account = await session.execute(
            select(self.model).where(
                (user_id_field == user.id) &
                (utility_type_id_field == utility_obj.id)
            )
        )
        return account.scalars().first()

    async def get_all_account(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> list[UserAccount]:
        """Получение всех счетов пользователя по telegram_id."""
        user: UserProfile = await user_crud.get_user_by_tg_id(
            session, telegram_id
        )
        if not user:
            return []
        return user.user_account


    async def delete_account(self):
        pass

    async def update_account(self):
        pass


user_account_crud = CRUDUserAccount(UserAccount)
