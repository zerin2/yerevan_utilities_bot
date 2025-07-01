import json
import os
from enum import Enum

from dotenv import load_dotenv
from exceptions import ValidationError
from redis import Redis

load_dotenv()

if os.getenv('DEBUG', None) == 'True':
    TELEGRAM_TOKEN = os.getenv('TEST_TELEGRAM_TOKEN')
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
else:
    TELEGRAM_TOKEN = os.getenv('DEPLOY_TELEGRAM_TOKEN')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)

REDIS_CLIENT = Redis(host=REDIS_HOST,
                     port=REDIS_PORT)

HIGH_REDIS_QUEUE_PARSER = 'high_queue_parser'
LOW_REDIS_QUEUE_PARSER = 'low_queue_parser'

HIGH_REDIS_QUEUE_BOT = 'high_queue_bot'
LOW_REDIS_QUEUE_BOT = 'low_queue_bot'

REDIS_BACKUP_QUEUE_NAME = 'backup_tasks'
REDIS_RESPONSE_BODY = {
    'tg_id': '',
    'task_id': '',
    'count': 1,
    'status': '',
    'notify': '',
    'account': '',
    'account_type': '',
    'city': '',
    'utility': '',
    'first_check': False,
    'response': {},
}
VALIDATOR_ERROR_TYPE = (ValidationError, json.JSONDecodeError)
CHECK_KEYS = ['tg_id', 'task_id', 'notify', 'count', 'status', 'account']


class ResponseStatusType(Enum):
    NEW = 'new'
    COMPLETE = 'complete'
    ERROR = 'error'
