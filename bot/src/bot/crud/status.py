from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
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
            status_name: str,
    ) -> Optional[StatusType]:
        """Возвращает статус по имени."""
        return self.get_by_field(session, 'name', status_name)

    async def create_status(
            self,
            session: AsyncSession,
            status: str,
    ) -> StatusType:
        """Создает статус."""
        return await self.create(session, {'name': status})


status_crud = CRUDStatus(StatusType)
