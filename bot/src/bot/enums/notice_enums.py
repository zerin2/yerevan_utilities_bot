from enum import StrEnum


class NoticeStateEnum(StrEnum):
    ON = 'on'
    OFF = 'off'

    @staticmethod
    def to_human(state: str) -> str:
        mapping = {
            NoticeStateEnum.ON.value: 'Включены',
            NoticeStateEnum.OFF.value: 'Выключены',
        }
        return mapping.get(state, 'Ошибочное состояние')


class NoticeTypeEnum(StrEnum):
    ANYTIME = 'anytime'
    PERIOD = 'period'

    @staticmethod
    def to_human(notice_type: str) -> str:
        mapping = {
            NoticeTypeEnum.ANYTIME.value: 'В любое время',
            NoticeTypeEnum.PERIOD.value: 'В период: ',
        }
        return mapping.get(notice_type, 'Ошибочный период')


class NoticeFlag(StrEnum):
    START = 'start'
    END = 'end'


class NoticeInterval(StrEnum):
    hour_00 = '00'
    hour_01 = '01'
    hour_02 = '02'
    hour_03 = '03'
    hour_04 = '04'
    hour_05 = '05'
    hour_06 = '06'
    hour_07 = '07'
    hour_08 = '08'
    hour_09 = '09'
    hour_10 = '10'
    hour_11 = '11'
    hour_12 = '12'
    hour_13 = '13'
    hour_14 = '14'
    hour_15 = '15'
    hour_16 = '16'
    hour_17 = '17'
    hour_18 = '18'
    hour_19 = '19'
    hour_20 = '20'
    hour_21 = '21'
    hour_22 = '22'
    hour_23 = '23'

    @staticmethod
    def to_human(hour: str) -> str:
        return 'error' if hour == 'error' else f'{hour}:00'
