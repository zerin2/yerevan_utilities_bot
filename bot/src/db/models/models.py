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

from db.models.base import BaseModel


class StatusType(BaseModel):
    """Тип статуса."""

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc='Название статуса. Должно быть уникальным.',
    )

    accounts_detail = relationship(
        'AccountsDetail',
        back_populates='status_type',
        doc='Связь с таблицей AccountsDetails. '
            'Определяет записи, использующие данный статус.',
    )
    user = relationship(
        'UsersProfile',
        back_populates='status_type',
        doc='Связь с таблицей UsersProfile.',
    )


class NoticeType(BaseModel):
    """Тип оповещения."""

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc='Название оповещения. Должно быть уникальным.',
    )

    user = relationship(
        'UsersProfile',
        back_populates='notice_type',
        doc='Связь с таблицей UsersProfile.',
    )
    accounts_detail = relationship(
        'AccountsDetail',
        back_populates='notice_type',
        doc='Связь с таблицей AccountsDetails.',
    )


class StartNoticeInterval(BaseModel):
    """Начальный интервал оповещения."""

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc='Начальный интервал оповещения. Должно быть уникальным.',
    )

    user = relationship(
        'UsersProfile',
        back_populates='start_notice_interval',
        doc='Связь с таблицей UsersProfile.',
    )


class EndNoticeInterval(BaseModel):
    """Конечный интервал оповещения."""

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc='Конечный интервал оповещения. Должно быть уникальным.',
    )

    user = relationship(
        'UsersProfile',
        back_populates='end_notice_interval',
        doc='Связь с таблицей UsersProfile.',
    )


class UtilitiesType(BaseModel):
    """Тип коммунальной услуги."""

    name = Column(String(50), unique=True, nullable=False, index=True,
                  doc='Название типа услуги. Должно быть уникальным.')

    accounts_detail = relationship(
        'AccountsDetail',
        back_populates='utilities_type',
        doc='Связь с таблицей AccountsDetails. '
            'Определяет записи, использующие данный тип услуги.',
    )


class UsersProfile(BaseModel):
    """Пользователи."""

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
        'UsersHistory',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    accounts_detail = relationship(
        'AccountsDetail',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    feedback = relationship(
        'Feedback',
        back_populates='user',
        cascade='all, delete-orphan',
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


class UsersHistory(BaseModel):
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

    user = relationship('UsersProfile', back_populates='history')


class City(BaseModel):
    """Названия городов."""

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    accounts_detail = relationship(
        'AccountsDetail',
        back_populates='city',
        doc='Связь с таблицей AccountsDetails.',
    )


class AccountsDetail(BaseModel):
    """Информация о коммунальных счетах пользователя.
    Хранит информацию об оплате, задолженностях и текущем статусе.
    """

    user_id = Column(
        Integer,
        ForeignKey('users_profile.id', ondelete='CASCADE'),
        index=True,
        doc='ID пользователя, связанный с записью. '
            'Удаление пользователя удаляет связанные записи.',
    )
    utility_type_id = Column(
        Integer,
        ForeignKey('utilities_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        doc='ID типа услуги. Если тип услуги удален, поле становится NULL.',
    )
    last_overpayment = Column(
        DECIMAL(15, 2),
        nullable=True,
        doc='(CREDIT) Последняя переплата пользователя. Значение в денежном формате.',
    )
    last_debt = Column(
        DECIMAL(15, 2),
        nullable=True,
        doc='(DEBIT) Последний долг пользователя. Значение в денежном формате.',
    )
    city_id = Column(
        Integer,
        ForeignKey('city.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        doc='ID названия города.',
    )
    address = Column(
        String,
        nullable=True,
        doc='Адрес.',
    )
    traffic = Column(
        String,
        nullable=True,
        doc='Показания счетчика.',
    )
    last_updated = Column(
        DateTime,
        default=func.now(),
        nullable=True,
        doc='Дата последнего обновления записи.',
    )
    notice_id = Column(
        Integer,
        ForeignKey('notice_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    status = Column(
        Integer,
        ForeignKey('status_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        doc='ID статуса. Если статус удален, поле становится NULL.',
    )
    info = Column(
        String,
        nullable=True,
        doc='Дополнительная информация о записи.',
    )

    user = relationship(
        'UsersProfile',
        back_populates='accounts_detail',
        doc='Связь с таблицей UsersProfile. '
            'Указывает на пользователя, которому принадлежит запись.',
    )
    utilities_type = relationship(
        'UtilitiesType',
        back_populates='accounts_detail',
        doc='Связь с таблицей UtilitiesType. Указывает тип услуги.',
    )
    notice_type = relationship(
        'NoticeType',
        back_populates='accounts_detail',
        doc='Связь с таблицей NoticeType. '
            'Указывает тип оповещения у пользователя.',
    )
    status_type = relationship(
        'StatusType',
        back_populates='accounts_detail',
        doc='Связь с таблицей StatusType. Указывает текущий статус записи.',
    )
    city = relationship(
        'City',
        back_populates='accounts_detail',
        doc='Связь с таблицей City. Указывает название города.',
    )


class Feedback(BaseModel):
    """Отзывы от пользователей, в том числе и ошибок."""

    user_id = Column(
        Integer,
        ForeignKey('users_profile.id', ondelete='CASCADE'),
        index=True,
    )
    type = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    status = Column(String(20), default='new')

    user = relationship('UsersProfile', back_populates='feedback')
