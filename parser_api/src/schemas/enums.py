from enum import Enum

EXAMPLE_FULL_REQUEST = {
    'example': {
        'tg_id': '123456789',
        'job_status': 'new',
        'notify': '1',
        'first_check': '1',
        'data': [
            {
                'account': '123',
                'account_type': 'code',
                'city': 'Ереван',
                'utility': 'electricity',
            },
            {
                'account': '0390315',
                'account_type': 'code',
                'city': 'Ереван',
                'utility': 'electricity',
            },
            {
                'account': '3-11-5-0-15',
                'account_type': 'code',
                'city': 'Ереван',
                'utility': 'water',
            },
            {
                'account': '830938',
                'account_type': 'code',
                'city': 'Ереван',
                'utility': 'gas',
            },
        ],
    },
}


class SchemaTitle(str, Enum):
    TG_ID = 'Telegram ID'
    JOB_STATUS = 'Статус задачи'
    DATA = 'Данные по лицевым счетам'
    NOTIFY = 'Признак уведомлений'
    FIRST_CHECK = 'Первичная проверка'
    ACCOUNT = 'Номер лицевого счёта'
    CITY = 'Город'
    ACCOUNT_TYPE = 'Тип счёта'
    UTILITY = 'Тип услуги'
    STATUS_RESPONSE = 'Статус ответа'
    RESPONSE = 'Ответ от сервиса'


class SchemaDescription(str, Enum):
    TG_ID = 'Уникальный идентификатор Telegram пользователя'
    JOB_STATUS = 'Текущий статус задачи по обработке данных'
    DATA = 'Список лицевых счетов, которые необходимо обработать'
    NOTIFY = 'Уведомлять пользователя о завершении задачи (1 - да, 0 - нет)'
    FIRST_CHECK = 'Флаг первичной проверки (1 - да, 0 - нет)'
    ACCOUNT = 'Номер лицевого счёта в системе коммунальных служб'
    CITY = 'Название города, к которому относится лицевой счёт'
    ACCOUNT_TYPE = 'Тип счёта (например, "code" или "phone")'
    UTILITY = 'Тип коммунальной услуги: "electricity", "water", "gas"'
    STATUS_RESPONSE = 'Результат последнего запроса по этому счёту'
    RESPONSE = 'Сырой ответ от сервиса, полученный при обработке'


class SchemaExample(str, Enum):
    TG_ID = '123456789'
    JOB_STATUS = 'new'
    NOTIFY = '1'
    FIRST_CHECK = '1'
    ACCOUNT = '0390315'
    CITY = 'Ереван'
    ACCOUNT_TYPE = 'code'
    UTILITY = 'electricity'
    STATUS_RESPONSE = '200'
    RESPONSE = '{"task_id": "2d8fe15e", "task_status": "processing"}'
