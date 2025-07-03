from enum import Enum


class FieldLength(int, Enum):
    TELEGRAM_ID = 50
    NAME = 50
    SETTINGS = 150
    ACCOUNT = 70
    ADDRESS = 150
    TRAFFIC = 100
    STATE_MESSAGE = 100
    FEEDBACK_TYPE = 60
    NOTICE_STATE = 10


class Status(Enum):
    NEW = 'new'
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class UserPersonalSettings(Enum):
    ACCOUNT_STATUS = 'account_status'
    NOTICE_STATE = 'notice_state'
    NOTICE_TYPE = 'notice_type'
