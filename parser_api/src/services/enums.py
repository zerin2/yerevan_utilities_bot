from enum import Enum

from core.settings import settings


class ProxySettings(Enum):
    PROXY_TEMPLATE = 'http://{proxy_address}:{port}'
    PROXY_ATTEMPT = 5
    RETRY_TIMEOUT_PROXY_LIST = 5
    GOOD_FAILURES = 3


class ProxyMessage(str, Enum):
    API_RATE_LIMITED = 'Превышено количество запросов на API'
    API_RESPONSE_ERROR = 'Ошибка API: статус ({response_status}), тело: ({text})'
    API_ERROR = 'Ошибка при работе с API: ({e})'
    BAD_RESPONSE = 'Некорректная структура ответа: ({data})'
    PROXY_LIST_OK = 'Добавлен новый прокси лист в кэш'
    PROXY_EMPTY_LIST_OK = 'Добавлен пустой прокси лист в кэш'
    PROXY_LIST_VALID_ERROR = 'Нет валидных прокси в списке: {proxy_list}'
    PROXY_LIST_ADD_ERROR = 'Ошибка добавления списка прокси в кэш. Ошибка: ({error})'
    EMPTY_KEY = 'Пустой ключ'
    LIST_NOT_FOUND = 'Список с прокси не найден'
    PROCESSING_LIST = 'Список в процессе запроса'


class WebshareProxy(Enum):
    TOKEN = settings.webshare_token
    URL_LIST = settings.webshare_url_list
    LIST_NAME = 'webshare_proxy_list'
    PARAMS_URL_LIST = {'mode': 'direct'}
    HEADERS = {'Authorization': 'Token ' + TOKEN}
    RESULT_KEY = 'results'


class LogerSettings(str, Enum):
    ROTATION = '10 MB'
    RETENTION = '7 days'
    LEVEL = 'DEBUG'


class LoggerMessage(str, Enum):
    NEW_MESSAGE = (
        'Поступила задача task_id: '
        '{task_id}, data: {data}, status: {status}'
    )
    BAD_STATUS_MESSAGE = (
        'Поступила задача с ошибочным статусом '
        'task_id: {task_id}, data: {data}, status: {status}'
    )


class TTL(int, Enum):
    REDIS_KEY = 60 * 60
    PROXY_LIST = 60 * 15


class AccountType(Enum):
    CODE = 'code'
    PHONE = 'phone'


class UtilityModelName(Enum):
    ELECTRICITY = 'electricity'
    GAS = 'gas'
    GAS_SERVICE = 'gas_service'
    WATER = 'water'
    VIVA_MTS = 'viva_mts'
    TEAM_TELECOM = 'team_telecom'
    U_COM = 'u_com'
    OVIO = 'ovio'


class StatusType(Enum):
    OK = 'ok'
    BAD = 'bad'
    NEW = 'new'
    PROCESSING = 'processing'
    COMPLETE = 'complete'
    ERROR = 'error'


class CityName(str, Enum):
    YEREVAN = 'ереван'
    ABOVYAN = 'абовян'
    ALAVERDI = 'алаверди'
    ANGEHAKOT = 'ангехакот'
    ARARAT = 'арарат'
    ARZNI = 'арзни'
    ARMAVIR = 'армавир'
    ARTASHAT = 'арташат'
    ARTIK = 'артик'
    AKHTALA = 'ахтала'
    ASHTARAK = 'аштарак'
    VANADZOR = 'ванадзор'
    VARDENIS = 'варденис'
    VAGHARSHAPAT = 'вагаршапат'
    GAVAR = 'гавар'
    GORIS = 'горис'
    GYUMRI = 'гюмри'
    DILIJAN = 'дилижан'
    IJEVAN = 'иджеван'
    KADJARAN = 'каджаран'
    KAPAN = 'капан'
    MARTUNI = 'мартуни'
    MEGHRI = 'мехри'
    RAZDAN = 'раздан'
    SEVAN = 'севан'
    SISIAN = 'сисиан'
    SPITAK = 'спитак'
    STEPANAVAN = 'степанаван'
    STEPANAKERT = 'степанакерт'
    TALIN = 'талин'
    TASHIR = 'ташир'
    CHARENTSAVAN = 'чаренцаван'
