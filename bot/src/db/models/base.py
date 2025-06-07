from sqlalchemy import Column, Integer

from db.core import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
