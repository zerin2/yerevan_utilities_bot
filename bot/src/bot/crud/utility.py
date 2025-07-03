from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.enums.utility_enums import UtilityName
from db.models.models import UtilityType


class CRUDUtility(CRUDBase):
    async def get_utility_by_id(
            self,
            session: AsyncSession,
            utility_id: id,
    ) -> Optional[UtilityType]:
        """Получение объекта коммунальной услуги по id."""
        return await self.get_by_id(session, utility_id)

    async def get_utility_by_name(
            self,
            session: AsyncSession,
            utility_name: UtilityName,
    ) -> Optional[UtilityType]:
        """Получение объекта коммунальной услуги по названию."""
        return await self.get_by_field(session, 'name', utility_name)

    async def create_utility(
            self,
            session: AsyncSession,
            utility_name: UtilityName,
    ) -> UtilityType:
        """Создает коммунальную услугу."""
        return await self.create(session, {'name': utility_name})

    async def get_or_create_utility(
            self,
            session: AsyncSession,
            utility_name: UtilityName,
    ) -> UtilityType:
        """Возвращает коммунальную услугу имени, если obj=None => создает."""
        utility_obj: UtilityType = await self.get_utility_by_name(session, utility_name)
        if utility_obj is None:
            return await self.create_utility(session, utility_name)
        return utility_obj


utility_crud = CRUDUtility(UtilityType)
