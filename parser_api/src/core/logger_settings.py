from loguru import logger

from core.settings import BASEDIR_PROJECT
from services.enums import LogerSettings

LOGS_PATH = BASEDIR_PROJECT / 'logs' / 'logs.log'
LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)

logger.add(
    str(LOGS_PATH),
    rotation=LogerSettings.ROTATION.value,
    retention=LogerSettings.RETENTION.value,
    enqueue=True,
)
