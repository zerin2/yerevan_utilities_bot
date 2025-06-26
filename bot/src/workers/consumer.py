import json
from dataclasses import dataclass

from enums.setting_enums import AccountStatus
from send_to_parser import DataStatus
from utils import to_decimal

import workers.config as conf
from bot.manager.composite_manager import CompositeManager
from db.core import async_session
from exceptions import JsonError, ParserError, StatusError, ValidationError
from logs.config import worker_logger
from workers.redis_task import RedisTask
from workers.tg_sender import BotSender
from workers.validators import check_data_keys

# {'tg_id': '259564426',
# 'task_id': '3f335481',
# 'count': 3,
# 'status': 'complete',
# 'notify': True,
# 'account': '0390315',
# 'account_type': 'code',
# 'utility': 'electricity',
# 'first_check': False,
# 'response': {'address': 'ք.ԵՐԵՎԱՆ ԳԱՐԵԳԻՆ ՆԺԴԵՀԻ փող., 5, 15',
# 'traffic': 'Ց-2.680, Գ-1.200/3561.630', 'debit': '0', 'credit': '332.55'}}

# {'tg_id': '259564426',
# 'task_id': '435148b3',
# 'count': 3,
# 'status': 'error',
# 'notify': True,
# 'account': '12321312',
# 'account_type': 'code',
# 'utility': 'gas',
# 'first_check': False,
# 'response': '(Account404) Аккаунт не найден'}


def f_test_consumer():
    HIGH_REDIS_QUEUE_PARSER = 'high_queue_parser'
    LOW_REDIS_QUEUE_PARSER = 'low_queue_parser'

    HIGH_REDIS_QUEUE_BOT = 'high_queue_bot'
    LOW_REDIS_QUEUE_BOT = 'low_queue_bot'
    while True:
        item = conf.REDIS_CLIENT.blpop([HIGH_REDIS_QUEUE_BOT,
                                        LOW_REDIS_QUEUE_BOT])
        if item is not None:
            queue_name, data_serialized = item
            data_str = data_serialized.decode('utf-8')
            data = json.loads(data_str)
            print("Имя очереди:", queue_name.decode('utf-8'))
            print("Получена задача:", data)


if __name__ == '__main__':
    f_test_consumer()


ERROR_LEN_MSG = 50


@dataclass
class TaskHandler(CompositeManager, BotSender):
    data: dict = None
    tg_id: str = None
    count: int = None
    utility: str = None
    status: str = None
    notify: bool = None
    response: dict = None
    first_check: bool = None

    def __post_init__(self):
        self.tg_id = self.data.get('tg_id')
        self.count = self.data.get('count')
        self.status = self.data.get('status')
        self.utility = self.data.get('utility')
        self.notify = self.data.get('notify')
        self.response = self.data.get('response')
        self.response = self.data.get('response')
        self.first_check = self.data.get('first_check')

    def handler(self):
        """

        """
        if self.first_check:
            self.first_solo_handler(self.data)
        elif self.status == conf.ResponseStatusType.ERROR.value:
            self.error_handler(self.data)
        elif self.status == conf.ResponseStatusType.COMPLETE.value:
            if self.count == 1:
                self.solo_handler(self.data)
            else:
                self.set_handler(self.data)

    async def first_solo_handler(self):
        pass

    async def solo_handler(self):
        async with async_session as session:
            account_repo = CompositeManager(session)
            user_account = await account_repo.edit_or_create_account_detail(
                tg_id=self.tg_id,
                utility_name=self.utility,
                last_overpayment=to_decimal(self.response.get('credit')),
                last_debt=to_decimal(self.response.get('debit')),
                address=self.response.get('address'),
                traffic=self.response.get('traffic'),
                status_name=AccountStatus.ACTIVE.value,
            )
            # todo: возвращаем через flush() => notice_id
            # todo: если at_change или notify=True, то отправляем оповещение

    def set_handler(self):
        pass

    def error_handler(self):
        pass


@dataclass
class InitWorker:
    data: dict = None
    validation_error: tuple = conf.VALIDATOR_ERROR_TYPE

    def __post_init__(self):
        self.data = {}


class Worker(InitWorker, DataStatus, RedisTask):
    async def main(self):
        item = self.get_priority_task()
        if item is not None:
            queue_name, data_serialized = item
            data_str = data_serialized.decode('utf-8')
            try:
                self.data = json.loads(data_str)
            except self.validation_error as e:
                error = f'Ошибка декодирования JSON: {str(e)[:ERROR_LEN_MSG]}'
                worker_logger.error(error)
                raise JsonError
            else:
                check_data_keys(self.data)
                worker_logger.info(f'Воркер взял задачу: {self.data}')
                # TODO: перенаправляем по статусу, ошибка, какая? далее отправка клиенту

    async def run(self):
        worker_logger.info('Worker_consumer_bot запущен.')
        while True:
            try:
                await self.main()
            except (ParserError, ValidationError, StatusError, Exception) as e:
                exc_name = e.__class__.__name__
                error_msg = f'({exc_name}) {str(e)}'
                worker_logger.exception(error_msg)
                self.error_task(self.data, error_msg)  # noqa
                # self.create_task_for_bot(self.data)

# if __name__ == '__main__':
#     worker = Worker()
#     asyncio.run(worker.run())
