from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.enums.notice_enums import NoticeTypeEnum
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
            notice_type_name: str,
    ) -> Optional[NoticeType]:
        """Получаем тип оповещения по имени."""
        return await self.get_by_field(session, 'name', notice_type_name)

    async def create_notice_type(
            self,
            session: AsyncSession,
            notice_type: str,
    ) -> NoticeType:
        """Создает тип оповещения."""
        return await self.create(session, {'name': notice_type})

    async def get_or_create_notice_type(
            self,
            session: AsyncSession,
            notice_type: NoticeTypeEnum,
    ) -> NoticeType:
        """Возвращает объект модели NoticeType, если obj=None => создает."""
        notice_type_obj: NoticeType = await self.get_notice_type_by_name(
            session, notice_type,
        )
        if notice_type_obj is None:
            return await self.create_notice_type(session, notice_type)
        return notice_type_obj


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
