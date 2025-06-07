from pathlib import Path

from pydantic_settings import BaseSettings

BASEDIR_OUT = Path(__file__).resolve().parents[3]
BASEDIR_PROJECT = Path(__file__).resolve().parents[1]
ENV_FILE_PATH = BASEDIR_OUT / 'infra' / '.env'

LOGS_PATH = BASEDIR_PROJECT / 'logs' / 'logs.log'
LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    """Конфигурация приложения."""

    test_redis_host: str
    redis_host: str
    redis_port: str
    redis_parser_db: int

    webshare_token: str
    webshare_login: str
    webshare_password: str

    api_parser_token: str
    debug: bool

    @property
    def get_redis_host(self) -> str:
        if self.debug:
            return self.test_redis_host
        return self.redis_host

    @property
    def redis_url(self) -> str:
        """Сформированная строка подключения к Redis."""
        if self.debug:
            return f'redis://{self.test_redis_host}:{self.redis_port}/{self.redis_parser_db}'
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_parser_db}'

    class Config:
        """Внутренние настройки класса Settings."""

        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()
