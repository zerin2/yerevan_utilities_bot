from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class NameMixin:
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc='Название должно быть уникальным.',
    )


class DateTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        doc='Дата создания записи.',
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        default=None,
        onupdate=datetime.now,
        doc='Дата последнего обновления записи.',
    )
