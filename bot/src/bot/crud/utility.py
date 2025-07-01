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
            utility_type: UtilityName,
    ) -> Optional[UtilityType]:
        """Получение объекта коммунальной услуги по названию."""
        return await self.get_by_field(session, 'name', utility_type)


utility_crud = CRUDUtility(UtilityType)