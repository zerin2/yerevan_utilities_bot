from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.enums.city_enums import CityName
from db.models.models import City


class CRUDUCity(CRUDBase):
    async def get_city_by_id(
            self,
            session: AsyncSession,
            city_id: id,
    ) -> Optional[City]:
        """Получение объекта модели City по id."""
        return await self.get_by_id(session, city_id)

    async def get_city_by_name(
            self,
            session: AsyncSession,
            city: CityName,
    ) -> Optional[City]:
        """Получение объекта модели City по названию."""
        return await self.get_by_field(session, 'name', city)


city_crud = CRUDUCity(City)