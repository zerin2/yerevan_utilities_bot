from enum import Enum


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
    REDIS_KEY = 3600


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
