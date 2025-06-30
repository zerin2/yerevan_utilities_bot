from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from db.models import EndNoticeInterval, NoticeType, StartNoticeInterval


class CRUDNotice(CRUDBase):
    async def get_notice_type_by_id(
            self,
            session: AsyncSession,
            notice_id: int,
    ) -> Optional[NoticeType]:
        """Получаем тип оповещения."""
        return await self.get_by_id(session, notice_id)

    async def get_notice_type_by_name(
            self,
            session: AsyncSession,
            notice_name: str,
    ) -> Optional[NoticeType]:
        """Получаем тип оповещения по имени."""
        return self.get_by_field(session, 'name', notice_name)

    async def create_notice_type(
            self,
            session: AsyncSession,
            notice_type: str,
    ) -> NoticeType:
        """Создает тип оповещения."""
        return await self.create(session, {'name': notice_type})


class CRUDBaseNoticeInterval(CRUDBase):
    async def get_interval_by_name(
            self,
            session: AsyncSession,
            notice_interval: str,
    ) -> Optional[StartNoticeInterval]:
        """Получаем тип оповещения по имени."""
        return await self.get_by_field(session, 'name', notice_interval)

    async def create_interval(
            self,
            session: AsyncSession,
            notice_interval: str,
    ) -> StartNoticeInterval:
        """Создает тип оповещения."""
        return await self.create(session, {'name': notice_interval})


class CRUDStartNoticeInterval(CRUDBaseNoticeInterval):
    """CRUD для начального интервала."""


class CRUDEndNoticeInterval(CRUDBaseNoticeInterval):
    """CRUD для конечного интервала."""


notice_type_crud = CRUDNotice(NoticeType)
start_notice_interval_crud = CRUDStartNoticeInterval(StartNoticeInterval)
end_notice_interval_crud = CRUDEndNoticeInterval(EndNoticeInterval)
