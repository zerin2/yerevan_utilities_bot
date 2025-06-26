from typing import TypeVar, Any, Generic, Optional, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.core import Base

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType]):
    """Базовый класс операций."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    def check_field_name(self, field_name: str) -> None:
        """Проверяет существование поля в модели."""
        if not hasattr(self.model, field_name):
            raise ValueError(
                f'Поле {field_name} не существует в модели {self.model.__name__}'
            )
        return None

    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """Получение объекта по id."""
        return await self.session.get(self.model, obj_id)

    async def get_by_field(
            self,
            field_name: str,
            value: Any,
    ) -> Optional[ModelType]:
        """Получение объекта по field_name и value."""
        self.check_field_name(field_name)
        field = getattr(self.model, field_name)
        db_obj = await self.session.execute(
            select(self.model).where(field == value)
        )
        return db_obj.scalars().first()

    async def get_multi(self) -> list[ModelType]:
        """Получение списка всех объектов модели."""
        db_objs = await self.session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            data: dict[str, Any],
    ) -> ModelType:
        """Создание объекта модели."""
        for field_name in data.keys():
            self.check_field_name(field_name)
        db_obj = self.model(**data)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def update_by_id(
            self,
            obj_id: int,
            data: dict[str, Any],
    ) -> ModelType:
        """Обновление объекта модели по id."""
        for field_name in data.keys():
            self.check_field_name(field_name)
        db_obj = await self.get_by_id(obj_id)
        if db_obj is None:
            raise ValueError(f'Объект с id={obj_id} не найден.')
        for field_name, value in data.items():
            setattr(db_obj, field_name, value)
        await self.session.flush()
        return db_obj

    async def update_by_field(
            self,
            field_name: str,
            value: Any,
            data: dict[str, Any],
    ) -> ModelType:
        """Обновление объекта модели по field_name и value."""
        for name in data.keys():
            self.check_field_name(name)
        db_obj = await self.get_by_field(field_name, value)
        if db_obj is None:
            raise ValueError(
                f'Объект с field_name={field_name}, '
                f'value={value} не найден.'
            )
        for field_name, value in data.items():
            setattr(db_obj, field_name, value)
        await self.session.flush()
        return db_obj

    async def remove(self, db_obj: ModelType) -> None:
        """Удаление объекта модели."""
        await self.session.delete(db_obj)
        await self.session.flush()

    async def remove_by_id(self, obj_id: int) -> None:
        """Удаление объекта модели по id."""
        db_obj = await self.get_by_id(obj_id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.flush()
