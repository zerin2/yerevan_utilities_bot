from enum import Enum, IntEnum, StrEnum

import aiogram.exceptions as exc


class Status(StrEnum):
    NEW = 'new'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ERROR = 'error'


class UserPersonalSettings(StrEnum):
    IS_DELIVERY_BLOCKED= 'is_delivery_blocked'
    STATUS = 'status_id'
    NOTICE_STATE = 'notice_state'
    NOTICE_TYPE = 'notice_type_id'


class FieldLength(IntEnum):
    TELEGRAM_ID = 50
    NAME = 50
    SETTINGS = 150
    ACCOUNT = 70
    ADDRESS = 150
    TRAFFIC = 100
    STATE_MESSAGE = 100
    FEEDBACK_TYPE = 60
    NOTICE_STATE = 10
    DELIVERY_ERROR = 30


class SendTelegramError(Enum):
    LITE_ERRORS = (
        exc.TelegramNetworkError,
        exc.TelegramRetryAfter,
    )
    CRITICAL_ERRORS = (
        exc.TelegramNotFound,
        exc.TelegramUnauthorizedError,
        exc.TelegramForbiddenError,
        Exception,
    )
