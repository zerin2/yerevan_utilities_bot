from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.crud.city import city_crud
from bot.crud.status import status_crud
from bot.crud.user import user_crud
from bot.crud.utility import utility_crud
from bot.enums.setting_enums import Status
from bot.enums.utility_enums import UtilityName
from db.models.models import (
    City,
    StatusType,
    UserAccount,
    UserProfile,
    UtilityType,
)
from settings import DEFAULT_UTILITIES, DEFAULT_EMPTY_ACCOUNT_VALUE


class CRUDUserAccount(CRUDBase):
    async def create_account(
            self,
            session: AsyncSession,
            telegram_id: str,
            account: str,
            utility_name: UtilityName,
            account_info: str = None,
            city_name: str = None,
            address: str = None,
            traffic: str = None,
            credit: Decimal = None,
            debit: Decimal = None,
            account_status: Status = Status.NEW.value,
    ) -> UserAccount:
        """Создает расчетный счет пользователя."""
        user_obj: UserProfile = await user_crud.get_or_create_user(
            session, telegram_id,
        )
        utility_obj: UtilityType = await utility_crud.get_or_create_utility(
            session, utility_name,
        )
        status_obj: StatusType = await status_crud.get_or_create_status(
            session, account_status,
        )
        city_obj: City = await city_crud.get_or_create_city(
            session, city_name,
        )
        return await self.create(
            session,
            dict(
                user_id=user_obj.id,
                account=account,
                account_info=account_info,
                utility_type_id=utility_obj.id,
                city_id=city_obj.id,
                address=address,
                traffic=traffic,
                credit=credit,
                debit=debit,
                status_id=status_obj.id,
            ),
        )

    async def create_default_accounts(
            self,
            session: AsyncSession,
            user_id: int,
            account: str = DEFAULT_EMPTY_ACCOUNT_VALUE,
            default_utilities: list = DEFAULT_UTILITIES,
    ) -> list[UserAccount]:
        """Создает дефолтные расчетные счета пользователя,
        параметры берутся из настроек проекта.
        """
        account_objects: list[UserAccount] = []
        for utility_name in default_utilities:
            account_objects.append(UserAccount(
                user_id=user_id,
                account=account,
                utility_name=utility_name,
            ))
        session.add_all(account_objects)
        return account_objects

    async def update_account(
            self,
            session: AsyncSession,
            telegram_id: str,
            utility: UtilityName,
            data: dict[str, Any],
    ) -> UserAccount:
        """Обновляет переданные поля в модели UserAccount."""
        account_obj: UserAccount = await self.get_account(
            session, telegram_id, utility,
        )
        return await self.update_by_id(
            session,
            account_obj.id,
            data,
        )

    async def get_account(
            self,
            session: AsyncSession,
            telegram_id: str,
            utility: UtilityName,
    ) -> Optional[UserAccount]:
        """Получение счета пользователя по utility_name и telegram_id."""
        user: UserProfile = await user_crud.get_user_by_tg_id(
            session, telegram_id,
        )
        utility_obj: UtilityType = await utility_crud.get_utility_by_name(
            session, utility,
        )
        if not user or not utility_obj:
            return None
        user_id_field = getattr(self.model, 'user_id')
        utility_type_id_field = getattr(self.model, 'utility_type_id')
        account = await session.execute(
            select(self.model).where(
                (user_id_field == user.id) &
                (utility_type_id_field == utility_obj.id),
            ),
        )
        return account.scalars().first()

    async def get_all_accounts(
            self,
            session: AsyncSession,
            telegram_id: str,
    ) -> list[UserAccount]:
        """Получение всех счетов пользователя по telegram_id."""
        user: UserProfile = await user_crud.get_user_by_tg_id(
            session, telegram_id,
        )
        if not user:
            return []
        result = await session.execute(
            select(UserAccount).where(UserAccount.user_id == user.id),
        )
        return result.scalars().all()

    async def delete_account(
            self,
            session: AsyncSession,
            telegram_id: str,
            utility: UtilityName,
    ) -> None:
        """Удаляет счет пользователя по utility_name и telegram_id."""
        account: UserAccount = await self.get_account(
            session, telegram_id, utility,
        )
        if not account:
            return None
        return await self.remove(session, account)


user_account_crud = CRUDUserAccount(UserAccount)
