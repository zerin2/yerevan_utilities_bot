from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.enums.feedback_enums import FeedbackStatus
from bot.enums.setting_enums import FieldLength
from db.models.base import BaseModel
from db.models.mixins import DateTimeMixin, NameMixin


class StatusType(BaseModel, NameMixin):
    """Тип статуса."""

    __tablename__ = 'status_type'

    user_account: Mapped['UserAccount'] = relationship(
        back_populates='status_type',
    )
    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='status_type',
    )


class NoticeType(BaseModel, NameMixin):
    """Тип оповещения."""

    __tablename__ = 'notice_type'

    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='notice_type',
    )
    user_account: Mapped['UserAccount'] = relationship(
        back_populates='notice_type',
    )


class StartNoticeInterval(BaseModel, NameMixin):
    """Начальный интервал оповещения."""

    __tablename__ = 'start_notice_interval'

    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='start_notice_interval',
    )


class EndNoticeInterval(BaseModel, NameMixin):
    """Конечный интервал оповещения."""

    __tablename__ = 'end_notice_interval'

    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='end_notice_interval',
    )


class City(BaseModel, NameMixin):
    """Названия городов."""

    __tablename__ = 'city'

    user_account: Mapped['UserAccount'] = relationship(
        back_populates='city',
    )


class UtilityType(BaseModel, NameMixin):
    """Тип коммунальной услуги."""

    __tablename__ = 'utility_type'

    user_account: Mapped['UserAccount'] = relationship(
        back_populates='utility_type',
    )


class UserProfile(BaseModel, DateTimeMixin):
    """Пользователи."""

    __tablename__ = 'user_profile'

    telegram_id: Mapped[str] = mapped_column(
        String(FieldLength.TELEGRAM_ID.value),
        unique=True,
        nullable=False,
        index=True,
    )
    settings: Mapped[Optional[str]] = mapped_column(
        String(FieldLength.SETTINGS.value),
        nullable=True,
    )
    is_delivery_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    status_id: Mapped[Optional[int]] = Column(
        Integer,
        ForeignKey('status_type.id', ondelete='SET NULL'),
        nullable=True,
    )
    notice_state: Mapped[str] = mapped_column(
        String(FieldLength.NOTICE_STATE.value),
        nullable=False,
    )
    notice_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('notice_type.id', ondelete='SET NULL'),
        nullable=False,
    )
    start_notice_interval_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('start_notice_interval.id', ondelete='SET NULL'),
        nullable=True,
    )
    end_notice_interval_id: Mapped[Optional[int]] = Column(
        Integer,
        ForeignKey('end_notice_interval.id', ondelete='SET NULL'),
        nullable=True,
    )

    history: Mapped[List['UserHistory']] = relationship(
        back_populates='user_profile',
        passive_deletes=True,
    )
    user_account: Mapped[List['UserAccount']] = relationship(
        back_populates='user_profile',
        passive_deletes=True,
    )
    feedback: Mapped[List['Feedback']] = relationship(
        back_populates='user_profile',
        passive_deletes=True,
    )
    status_type: Mapped['StatusType'] = relationship(
        back_populates='user_profile',
    )
    notice_type: Mapped['NoticeType'] = relationship(
        back_populates='user_profile',
    )
    start_notice_interval: Mapped['StartNoticeInterval'] = relationship(
        back_populates='user_profile',
    )
    end_notice_interval: Mapped['EndNoticeInterval'] = relationship(
        back_populates='user_profile',
    )


class UserAccount(BaseModel, DateTimeMixin):
    """Информация о коммунальных счетах пользователя.
    Хранит информацию об оплате, задолженностях и текущем статусе.
    """

    __tablename__ = 'user_account'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_profile.id', ondelete='CASCADE'),
        index=True,
    )
    account: Mapped[str] = mapped_column(
        String(FieldLength.ACCOUNT.value),
        nullable=False,
        index=True,
        doc='Расчетный счет пользователя.',
    )
    account_info: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        doc='Дополнительная информация об аккаунте.',
    )
    utility_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('utility_type.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        doc='(fk) коммунальной услуги.',
    )
    city_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('city.id', ondelete='SET NULL'),
        nullable=True,
        doc='(fk) города.',
    )
    address: Mapped[Optional[str]] = mapped_column(
        String(FieldLength.ADDRESS.value),
        nullable=True,
        doc='Адрес.',
    )
    traffic: Mapped[Optional[str]] = mapped_column(
        String(FieldLength.TRAFFIC.value),
        nullable=True,
        doc='Показания счетчика.',
    )
    credit: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
        doc='(CREDIT) Последняя переплата пользователя.',
    )
    debit: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
        doc='(DEBIT) Последний долг пользователя.',
    )
    status_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('status_type.id', ondelete='SET NULL'),
        nullable=True,
        doc='(fk) статуса пользователя.',
    )

    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='user_account',
    )
    utility_type: Mapped['UtilityType'] = relationship(
        back_populates='user_account',
    )
    notice_type: Mapped['NoticeType'] = relationship(
        back_populates='user_account',
    )
    status_type: Mapped['StatusType'] = relationship(
        back_populates='user_account',
    )
    city: Mapped['City'] = relationship(
        back_populates='user_account',
    )


class UserHistory(BaseModel, DateTimeMixin):
    """История запросов юзеров."""

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user_profile.id', ondelete='CASCADE'),
        index=True,
    )
    chat_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    message_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    message_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    state: Mapped[Optional[str]] = Column(
        String(FieldLength.STATE_MESSAGE.value),
        nullable=True,
    )

    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='history',
    )


class Feedback(BaseModel, DateTimeMixin):
    """Отзывы от пользователей, в том числе и ошибок."""

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user_profile.id', ondelete='CASCADE'),
        index=True,
    )
    feedback_type: Mapped[str] = mapped_column(
        String(FieldLength.FEEDBACK_TYPE.value),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String,
        default=FeedbackStatus.NEW.value,
    )

    user_profile: Mapped['UserProfile'] = relationship(
        back_populates='feedback',
                                                       )
