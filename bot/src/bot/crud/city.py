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
            city_name: CityName,
    ) -> Optional[City]:
        """Получение объекта модели City по названию."""
        return await self.get_by_field(session, 'name', city_name)

    async def create_city(
            self,
            session: AsyncSession,
            city_name: CityName,
    ) -> City:
        """Создает объект модели City."""
        return await self.create(session, {'name': city_name})

    async def get_or_create_city(
            self,
            session: AsyncSession,
            city_name: CityName,
    ) -> City:
        """Возвращает объект модели City, если obj=None => создает."""
        city_obj: City = await self.get_city_by_name(session, city_name)
        if city_obj is None:
            return await self.create_city(session, city_name)
        return city_obj


city_crud = CRUDUCity(City)
