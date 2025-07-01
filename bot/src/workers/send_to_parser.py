import asyncio
import copy
import uuid
from dataclasses import dataclass
from enum import Enum

from enums.city_enums import CityName
from exceptions import EmptyKeyError, StatusError
from loguru import logger

import workers.config as conf
from bot.manager.composite_manager import CompositeManager
from db.core import async_session
from settings import ACCOUNT_TYPE
from workers.redis_task import RedisTask


@dataclass
class DataStatus:
    status_new: str = conf.ResponseStatusType.NEW.value
    status_error: str = conf.ResponseStatusType.ERROR.value
    status_complete: str = conf.ResponseStatusType.COMPLETE.value

    def is_complete_status(self, data: dict) -> None:
        if data.get('status') != self.status_complete:
            error = f'Статус задачи не {self.status_complete}'
            logger.error(error)
            raise StatusError(error)

    def complete_task(self, data: dict, parser_response: dict | str) -> dict:
        data['status'] = self.status_complete
        data['response'] = parser_response
        return data

    def error_task(self, data: dict, error_message: str) -> dict:
        data['status'] = self.status_error
        data['response'] = error_message
        return data

    def new_task(self, data: dict) -> dict:
        data['status'] = self.status_error
        return data


class ArgumentType(str, Enum):
    ONE = 'one'
    ALL = 'all'


@dataclass
class ParserTaskBuilder(DataStatus, RedisTask):
    tg_id: str = None  # обязательное
    account_mode: ArgumentType = ArgumentType.ONE  # обязательное
    notify: bool = True
    account: str = None
    utility: str = None
    city: str = None
    user_accounts: dict = None
    first_check: bool = False

    def __post_init__(self):
        RedisTask.__post_init__(self)

        if self.account_mode == ArgumentType.ONE:
            check_list = [self.tg_id, self.account, self.utility]
            if any(var is None for var in check_list):
                raise EmptyKeyError(f'Нет ключей {check_list}')
        else:
            if self.tg_id is None:
                raise EmptyKeyError('Нет ключа "tg_id"')
            if self.account or self.utility:
                raise KeyError(f'При account_mode = "{ArgumentType.ALL.value}" '
                               f'значения: "account" и "utility" не нужны')

    async def get_user_accounts(self):
        async with async_session() as session:
            manager = CompositeManager(session)
            self.user_accounts = await manager.get_all_account_by_tg_id(self.tg_id)

    async def data_account_count(self):
        await self.get_user_accounts()
        return len([_ for _ in self.user_accounts.values() if _ is not None])

    def init_task(self, account, account_type, city, count, utility):
        data = copy.deepcopy(conf.REDIS_RESPONSE_BODY)
        data['tg_id'] = self.tg_id
        data['task_id'] = str(uuid.uuid4())[:8]
        data['notify'] = self.notify
        data['count'] = count
        data['status'] = self.status_new
        data['account'] = account
        data['account_type'] = account_type
        data['city'] = city
        data['utility'] = utility
        data['first_check'] = self.first_check
        return data

    async def create_task_to_parser(self, priority: str) -> None:
        """

        """
        if priority not in ('high', 'low'):
            raise ValueError('priority должен быть \'high\' или \'low\'')

        if self.account_mode == ArgumentType.ONE:
            self.create_task(
                self.init_task(
                    account=self.account,
                    account_type=ACCOUNT_TYPE[self.utility],
                    count=1,
                    utility=self.utility,
                    city=self.city,
                ),
                priority,
                'parser',
            )
        else:
            user_account_count = await self.data_account_count()
            for utility_name, account_number in self.user_accounts.items():
                if account_number is not None:
                    self.create_task(
                        self.init_task(
                            account=account_number,
                            account_type=ACCOUNT_TYPE[utility_name],
                            count=user_account_count,
                            utility=utility_name,
                            city=self.city,
                        ),
                        priority,
                        'parser',
                    )


async def main():
    from src.enums.scene_enums import UtilityModelName
    a = ParserTaskBuilder(
        tg_id='259564426',  # 259564426 | 93064880
        account='0390315',  # 0390315 | 12321312
        utility=UtilityModelName.ELECTRICITY.value,
        account_mode='one',  # all | one
        city=CityName.YEREVAN.value,
    )
    await a.create_task_to_parser('high')
    # for _ in range(5):
    #     await a.create_task_to_parser('high')


asyncio.run(main())
