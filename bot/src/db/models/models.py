from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DECIMAL,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.enums.setting_enums import FieldLength
from db.models.base import BaseModel
from db.models.mixin import NameMixin, DateTimeMixin


class StatusType(BaseModel, NameMixin):
    """Тип статуса."""

    __tablename__ = 'status_type'

    account_detail: Mapped['UserAccount'] = relationship(
        back_populates='status_type',
        doc='Определяет записи, использующие данный статус.',
    )
    user: Mapped['UserProfile'] = relationship(
        back_populates='status_type',
        doc='Связь с таблицей UserProfile.',
    )


class NoticeType(BaseModel, NameMixin):
    """Тип оповещения."""

    __tablename__ = 'notice_type'

    user = relationship(
        'UserProfile',
        back_populates='notice_type',
        doc='Связь с таблицей UserProfile.',
    )
    account_detail = relationship(
        'AccountDetail',
        back_populates='notice_type',
        doc='Связь с таблицей AccountDetail.',
    )


class StartNoticeInterval(BaseModel, NameMixin):
    """Начальный интервал оповещения."""

    __tablename__ = 'start_notice_interval'

    user = relationship(
        'UserProfile',
        back_populates='start_notice_interval',
        doc='Связь с таблицей UserProfile.',
    )


class EndNoticeInterval(BaseModel, NameMixin):
    """Конечный интервал оповещения."""

    __tablename__ = 'end_notice_interval'

    user = relationship(
        'UserProfile',
        back_populates='end_notice_interval',
        doc='Связь с таблицей UserProfile.',
    )


class UtilityType(BaseModel, NameMixin):
    """Тип коммунальной услуги."""

    __tablename__ = 'utility_type'

    account_detail = relationship(
        'AccountDetail',
        back_populates='utility_type',
        doc='Связь с таблицей AccountDetail. '
            'Определяет записи, использующие данный тип услуги.',
    )


class UserProfile(BaseModel):
    """Пользователи."""

    __tablename__ = 'user_profile'

    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    settings = Column(String(150), nullable=True)
    is_delivery_blocked = Column(String(50), nullable=True)
    status_id = Column(
        Integer,
        ForeignKey('status_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    notice_state = Column(
        String(30), nullable=True,
    )
    notice_type_id = Column(
        Integer,
        ForeignKey('notice_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    start_notice_interval_id = Column(
        Integer,
        ForeignKey('start_notice_interval.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    end_notice_interval_id = Column(
        Integer,
        ForeignKey('end_notice_interval.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    electricity = Column(String(50), nullable=True)
    gas = Column(String(50), nullable=True)
    gas_service = Column(String(50), nullable=True)
    water = Column(String(50), nullable=True)
    viva_mts = Column(String(50), nullable=True)
    team_telecom = Column(String(50), nullable=True)
    u_com = Column(String(50), nullable=True)
    ovio = Column(String(50), nullable=True)

    history = relationship(
        'UserHistory',
        back_populates='user',
        passive_deletes=True,
    )
    account_detail = relationship(
        'AccountDetail',
        back_populates='user',
        passive_deletes=True,
    )
    feedback = relationship(
        'Feedback',
        back_populates='user',
        passive_deletes=True,
    )
    status_type = relationship(
        'StatusType',
        back_populates='user',
        doc='Связь с таблицей StatusType. '
            'Указывает статус пользователя.',
    )
    notice_type = relationship(
        'NoticeType',
        back_populates='user',
        doc='Связь с таблицей NoticeType. '
            'Указывает тип оповещения у пользователя.',
    )
    start_notice_interval = relationship(
        'StartNoticeInterval',
        back_populates='user',
        doc='Связь с таблицей NoticeType. '
            'Указывает начальный интервал оповещения у пользователя.',
    )
    end_notice_interval = relationship(
        'EndNoticeInterval',
        back_populates='user',
        doc='Связь с таблицей NoticeType. '
            'Указывает конечный интервал оповещения у пользователя.',
    )


class UserHistory(BaseModel):
    """История запросов юзеров."""

    user_id = Column(
        Integer,
        ForeignKey('users_profile.id', ondelete='CASCADE'),
        index=True,
    )
    chat_id = Column(Integer)
    message_id = Column(Integer)
    message_content = Column(Text, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    user = relationship('UserProfile', back_populates='history')


class City(BaseModel, NameMixin):
    """Названия городов."""

    __tablename__ = 'city'

    account_detail = relationship(
        'AccountDetail',
        back_populates='city',
        doc='Связь с таблицей AccountDetail.',
    )


class UserAccount(BaseModel, DateTimeMixin):
    """Информация о коммунальных счетах пользователя.
    Хранит информацию об оплате, задолженностях и текущем статусе.
    """
    __tablename__ = 'user_account'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_profile.id', ondelete='CASCADE'),
        index=True,
        doc='ID пользователя, связанный с записью. '
            'Удаление пользователя удаляет связанные записи.',
    )
    account: Mapped[str] = mapped_column(
        String(FieldLength.ACCOUNT.value),
        nullable=False,
        index=True,
        doc='Расчетный счет пользователя.'
    )
    account_info: Mapped[str] = mapped_column(
        String,
        nullable=True,
        doc='Дополнительная информация о счете.',
    )
    utility_type_id: Mapped[int] = mapped_column(
        ForeignKey('utility_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        doc='ID типа услуги. Если тип услуги удален, поле становится NULL.',
    )
    city_id: Mapped[int]  = mapped_column(
        ForeignKey('city.id', ondelete='SET NULL'),
        nullable=True,
        doc='ID названия города.',
    )
    address: Mapped[str] = mapped_column(
        String(FieldLength.ADDRESS.value),
        nullable=True,
        doc='Адрес.',
    )
    traffic: Mapped[str] = mapped_column(
        String(FieldLength.TRAFFIC.value),
        nullable=True,
        doc='Показания счетчика.',
    )
    credit = Column(
        DECIMAL(15, 2),
        nullable=True,
        doc='(CREDIT) Последняя переплата пользователя. '
            'Значение в денежном формате.',
    )
    debit = Column(
        DECIMAL(15, 2),
        nullable=True,
        doc='(DEBIT) Последний долг пользователя. '
            'Значение в денежном формате.',
    )


    status = Column(
        Integer,
        ForeignKey('status_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        doc='ID статуса. Если статус удален, поле становится NULL.',
    )


    user = relationship(
        'UsersProfile',
        back_populates='account_detail',
        doc='Связь с таблицей UsersProfile. '
            'Указывает на пользователя, которому принадлежит запись.',
    )
    utility_type = relationship(
        'UtilityType',
        back_populates='account_detail',
        doc='Связь с таблицей UtilityType. Указывает тип услуги.',
    )
    notice_type = relationship(
        'NoticeType',
        back_populates='account_detail',
        doc='Связь с таблицей NoticeType. '
            'Указывает тип оповещения у пользователя.',
    )
    status_type = relationship(
        'StatusType',
        back_populates='account_detail',
        doc='Связь с таблицей StatusType. Указывает текущий статус записи.',
    )
    city = relationship(
        'City',
        back_populates='account_detail',
        doc='Связь с таблицей City. Указывает название города.',
    )


class Feedback(BaseModel):
    """Отзывы от пользователей, в том числе и ошибок."""

    user_id = Column(
        Integer,
        ForeignKey('user_profile.id', ondelete='CASCADE'),
        index=True,
    )
    type: Mapped[str] = mapped_column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    status = Column(String(20), default='new')

    user = relationship('UserProfile', back_populates='feedback')
