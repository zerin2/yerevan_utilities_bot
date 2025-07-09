from pathlib import Path

from pydantic_settings import BaseSettings

from bot.enums.notice_enums import NoticeStateEnum, NoticeTypeEnum
from bot.enums.scene_enums import UtilityName
from bot.enums.setting_enums import (
    Status,
    UserPersonalSettings,
)
from bot.enums.utility_enums import UtilityType

BASEDIR_OUT = Path(__file__).resolve().parents[2]
BASEDIR_PROJECT = Path(__file__).resolve().parents[1]
ENV_FILE_PATH = BASEDIR_OUT / 'infra' / '.env'

LOGS_PATH = BASEDIR_PROJECT / 'logs'
LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)
BOT_LOG_PATH = LOGS_PATH / 'bot/bot_logs.log'
PROVIDERS_LOG_PATH = LOGS_PATH / 'providers/providers_logs.log'
WORKER_LOG_PATH = LOGS_PATH / 'providers/worker_logs.log'


class Settings(BaseSettings):
    """Конфигурация приложения."""

    debug: bool
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str

    redis_test_host: str
    redis_host: str
    redis_port: str
    redis_parser_db: int

    telegram_test_token: str
    telegram_deploy_token: str
    telegram_admin_login: str
    telegram_admin_password: str

    api_parser_token: str
    api_url: str
    api_test_url: str

    @property
    def telegram_token(self) -> str:
        """Получение телеграм токена."""
        if self.debug:
            return self.telegram_test_token
        return self.telegram_deploy_token

    @property
    def database_url(self) -> str:
        """Сформированная строка подключения к базе данных."""
        return (
            f'postgresql+asyncpg://{self.db_user}:'
            f'{self.db_password}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )

    @property
    def get_redis_host(self) -> str:
        if self.debug:
            return self.redis_test_host
        return self.redis_host

    @property
    def redis_url(self) -> str:
        """Сформированная строка подключения к Redis."""
        if self.debug:
            return (
                f'redis://'
                f'{self.redis_test_host}'
                f':{self.redis_port}'
                f'/{self.redis_parser_db}'
            )
        return (
            f'redis://'
            f'{self.redis_host}'
            f':{self.redis_port}'
            f'/{self.redis_parser_db}'
        )

    @property
    def get_api_url(self) -> str:
        """Получение url для подключения к API."""
        if self.debug:
            return self.api_test_url
        return self.api_url

    class Config:
        """Внутренние настройки класса Settings."""

        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
        extra = 'ignore'


ACCOUNT_TYPE = {
    UtilityName.ELECTRICITY: UtilityType.CODE.value,
    UtilityName.GAS: UtilityType.CODE.value,
    UtilityName.GAS_SERVICE: UtilityType.CODE.value,
    UtilityName.WATER: UtilityType.CODE.value,
    UtilityName.VIVA_MTS: UtilityType.PHONE.value,
    UtilityName.TEAM_TELECOM: UtilityType.PHONE.value,
    UtilityName.U_COM: UtilityType.PHONE.value,
    UtilityName.OVIO: UtilityType.PHONE.value,
}

DEFAULT_UTILITIES = [
    UtilityName.ELECTRICITY.value,
    UtilityName.GAS.value,
    UtilityName.GAS_SERVICE.value,
    UtilityName.WATER.value,
]

DEFAULT_PERSONAL_SETTINGS = {
    UserPersonalSettings.IS_DELIVERY_BLOCKED.value: False,
    UserPersonalSettings.STATUS.value: Status.NEW.value,
    UserPersonalSettings.NOTICE_STATE.value: NoticeStateEnum.ON.value,
    UserPersonalSettings.NOTICE_TYPE.value: NoticeTypeEnum.ANYTIME.value,
}

settings = Settings()
