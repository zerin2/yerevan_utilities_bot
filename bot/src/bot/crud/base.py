from typing import Type, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

import db.models as model
from bot.handle_errors import handle_db_errors


class BaseRepository:
    """Базовый репозиторий."""

    USER_PROFILE_MODEL = model.UsersProfile
    USER_HISTORY_MODEL = model.UsersHistory
    STATUS_TYPE_MODEL = model.StatusType
    START_NOTICE_INTERVAL_MODEL = model.StartNoticeInterval
    END_NOTICE_INTERVAL_MODEL = model.EndNoticeInterval
    NOTICE_TYPE_MODEL = model.NoticeType
    UTILITIES_TYPE_MODEL = model.UtilitiesType
    ACCOUNTS_DETAILS_MODEL = model.AccountsDetail
    FEEDBACK_MODEL = model.Feedback

    def __init__(self, session: AsyncSession):
        self.session = session


class BaseBotManager(BaseRepository):
    """Базовый менеджер, с основными методами работы с бд.
    Большинство ошибок обрабатывается в '@handle_db_errors'.
    """

    ModelType = TypeVar('ModelType', bound=DeclarativeMeta)

    @staticmethod
    def check_variable(*variables: str | int) -> None:
        """Проверяет, что переменные не являются None, нулевым числом.
        Выбрасывает ValueError, если условие нарушено.
        """
        for variable in variables:
            if variable is None:
                raise ValueError(
                    'Передано значение None в одну из переменных.',
                )
            if isinstance(variable, int) and variable <= 0:
                raise ValueError(
                    f'Передано значение меньше или равное нулю: {variable}.',
                )

    @handle_db_errors
    async def is_exist(
            self,
            model: Type[ModelType],
            field_name: str,
            variable: str | int,
    ) -> bool:
        """Проверяет, существует ли запись в бд для заданной модели,
        имени поля и значения переменной.
        Возвращает True, если запись существует, иначе False.
        """
        self.check_variable(variable)
        field = getattr(model, field_name)
        result = await self.session.execute(
            select(model)
            .where(field == variable),
        )
        variable_is_exist = result.scalars().first()
        return variable_is_exist is not None

    @handle_db_errors
    async def is_exist_fields(
            self,
            model: Type[ModelType],
            fields: dict,
    ) -> bool:
        """Проверяет, существуют ли записи в бд
        для всех полей в переданном словаре.
        """
        for field_name, value in fields.items():
            self.check_variable(value)
            if not await self.is_exist(model, field_name, value):
                return False
        return True

    @handle_db_errors
    async def get_by_field(
            self,
            model: Type[ModelType],
            field_name: str,
            variable: str | int,
    ) -> ModelType | None:
        """Получает запись из бд для заданной модели,
        где значение указанного поля совпадает с переданным значением.
        """
        self.check_variable(variable)
        field = getattr(model, field_name)
        result = await self.session.execute(
            select(model)
            .where(field == variable),
        )
        value = result.scalars().first()
        return value

    @handle_db_errors
    async def delete_instance(
            self,
            model: Type[ModelType],
            field_name: str,
            variable: str | int,
    ) -> None:
        """Удаление записи из базы данных для указанной модели
        по заданному полю и значению.
        """
        self.check_variable(variable)
        field = getattr(model, field_name)
        await self.session.execute(
            delete(model)
            .where(field == variable),
        )

    @handle_db_errors
    async def add_new_instance(
            self,
            model: Type[ModelType],
            fields: dict[str, str | int],
    ) -> ModelType | None:
        """Добавление новой записи в базу данных
        для указанной модели с переданными полями.
        """
        for field_name, value in fields.items():
            self.check_variable(value)
        instance = model(**fields)
        self.session.add(instance)
        return instance

    @handle_db_errors
    async def edit_one_value(
            self,
            model: Type[ModelType],
            field_name: str,
            value: int | str,
            update_field_name: str,
            new_value: str | int,
    ) -> ModelType | None:
        """Обновляет указанное поле записи модели в базе данных.
        Параметры:
        ----------
        model : Type[ModelType]
            Модель SQLAlchemy для обновления.
        field_name : str
            Поле для поиска записи (например, 'id').
        value : int | str
            Значение для поиска записи.
        update_field_name : str
            Поле, которое нужно обновить.
        new_value : str | int
            Новое значение для указанного поля.
        Возвращает:
        ----------
        ModelType | None
        Обновленный экземпляр модели или None,
        если запись не найдена или возникла ошибка.
        """
        instance = await self.get_by_field(model, field_name, value)
        if instance is None:
            return None
        setattr(instance, update_field_name, new_value)
        return instance

    @handle_db_errors
    async def edit_or_create_values(
            self,
            model: Type[ModelType],
            field_name: str,
            value: int | str,
            new_values: dict[str, str | int],
    ) -> ModelType | None:
        """Редактирует существующую запись или создаёт новую,
        если запись не найдена.
        """
        instance = await self.get_by_field(model, field_name, value)
        if instance is None:
            instance = model(**new_values)
            self.session.add(instance)
            await self.session.flush()
            return instance
        for key, val in new_values.items():
            setattr(instance, key, val)
        return instance
