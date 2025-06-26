from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.core import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
