from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.enums.setting_enums import Status
from db.models import StatusType


class CRUDStatus(CRUDBase):
    async def get_status_by_id(
            self,
            session: AsyncSession,
            status_id: int,
    ) -> Optional[StatusType]:
        """Возвращает статус."""
        return await self.get_by_id(session, status_id)

    async def get_status_by_name(
            self,
            session: AsyncSession,
            status_name: Status,
    ) -> Optional[StatusType]:
        """Возвращает статус по имени."""
        return await self.get_by_field(session, 'name', status_name)

    async def create_status(
            self,
            session: AsyncSession,
            status_name: Status,
    ) -> StatusType:
        """Создает статус."""
        return await self.create(session, {'name': status_name})

    async def get_or_create_status(
            self,
            session: AsyncSession,
            status_name: Status,
    ) -> StatusType:
        """Возвращает статус по имени, если obj=None => создает."""
        status_obj: StatusType = await self.get_status_by_name(session, status_name)
        if status_obj is None:
            return await self.create_status(session, status_name)
        return status_obj


status_crud = CRUDStatus(StatusType)
