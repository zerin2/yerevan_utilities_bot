from pathlib import Path

from pydantic_settings import BaseSettings

from bot.enums.notice_enums import NoticeState, NoticeType
from bot.enums.scene_enums import UtilityName
from bot.enums.setting_enums import (
    Status,
    UserPersonalSettings,
)
from bot.enums.utility_enums import UtilityType

BASEDIR_OUT = Path(__file__).resolve().parents[2]
BASEDIR_PROJECT = Path(__file__).resolve().parents[1]
ENV_FILE_PATH = BASEDIR_OUT / 'infra' / '.env'


class Settings(BaseSettings):
    """Конфигурация приложения."""

    test_telegram_token: str
    deploy_telegram_token: str

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str

    test_redis_host: str
    redis_host: str
    redis_port: str

    debug: bool

    @property
    def telegram_token(self) -> str:
        """Формирование телеграм токена."""
        if self.debug:
            return self.test_telegram_token
        return self.deploy_telegram_token

    @property
    def database_url(self) -> str:
        """Сформированная строка подключения к базе данных."""
        return (
            f'postgresql+asyncpg://{self.db_user}:'
            f'{self.db_password}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )

    @property
    def redis_url(self) -> str:
        """Сформированная строка подключения к Redis."""
        if self.debug:
            return f'redis://{self.test_redis_host}:{self.redis_port}/0'
        return f'redis://{self.redis_host}:{self.redis_port}/0'

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

DEFAULT_PERSONAL_SETTINGS = {
    UserPersonalSettings.ACCOUNT_STATUS.value: Status.NEW.value,
    UserPersonalSettings.NOTICE_STATE.value: NoticeState.ON.value,
    UserPersonalSettings.NOTICE_TYPE.value: NoticeType.ANYTIME.value,
}

settings = Settings()
