from pathlib import Path

from pydantic_settings import BaseSettings

from bot.enums.scene_enums import UtilityModelName
from bot.enums.setting_enums import (
    AccountStatus,
    NoticeState,
    NoticeType,
    PersonalSettings,
    UtilityType,
)

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
    UtilityModelName.ELECTRICITY: UtilityType.CODE.value,
    UtilityModelName.GAS: UtilityType.CODE.value,
    UtilityModelName.GAS_SERVICE: UtilityType.CODE.value,
    UtilityModelName.WATER: UtilityType.CODE.value,
    UtilityModelName.VIVA_MTS: UtilityType.PHONE.value,
    UtilityModelName.TEAM_TELECOM: UtilityType.PHONE.value,
    UtilityModelName.U_COM: UtilityType.PHONE.value,
    UtilityModelName.OVIO: UtilityType.PHONE.value,
}

PERSONAL_SETTINGS = {
    PersonalSettings.ACCOUNT_STATUS.value: AccountStatus.NEW.value,
    PersonalSettings.NOTICE_STATE.value: NoticeState.ON.value,
    PersonalSettings.NOTICE_TYPE.value: NoticeType.ANYTIME.value,
}
""" PERSONAL_SETTINGS (dict): Настройки по умолчанию для новых пользователей. """

settings = Settings()
