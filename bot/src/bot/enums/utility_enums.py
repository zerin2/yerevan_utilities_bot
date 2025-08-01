from enum import StrEnum


class UtilityType(StrEnum):
    CODE = 'code'
    PHONE = 'phone'


class UtilityName(StrEnum):
    ELECTRICITY = 'electricity'
    GAS = 'gas'
    GAS_SERVICE = 'gas_service'
    WATER = 'water'
    VIVA_MTS = 'viva_mts'
    TEAM_TELECOM = 'team_telecom'
    U_COM = 'u_com'
    OVIO = 'ovio'


class UtilityIcon(StrEnum):
    LIGHTNING = '⚡'
    FIRE = '🔥'
    TOOLS = '🛠️'
    DROP = '💧'
    PHONE = '📱'
    HANDSET = '📞'
    INTERNET = '🌐'
    TV = '📺'


class UtilityRUS(StrEnum):
    ELECTRICITY_RUS = ' Электричество '
    GAS_RUS = ' Газ '
    GAS_SERVICE_RUS = ' Газ (обслуживание) '
    WATER_RUS = ' Вода '
    VIVA_MTS_RUS = ' VIVA (MTS) '
    TEAM_TELECOM_RUS = 'team (Telecom Armenia) '
    U_COM_RUS = ' U! com '
    OVIO_RUS = ' OVIO | Rostelecom '


class UtilityLabel(StrEnum):
    ELECTRICITY = UtilityRUS.ELECTRICITY_RUS.value + UtilityIcon.LIGHTNING.value
    GAS = UtilityRUS.GAS_RUS.value + UtilityIcon.FIRE.value
    GAS_SERVICE = UtilityRUS.GAS_SERVICE_RUS.value + UtilityIcon.TOOLS.value
    WATER = UtilityRUS.WATER_RUS.value + UtilityIcon.DROP.value
    VIVA_MTS = UtilityRUS.VIVA_MTS_RUS.value + UtilityIcon.PHONE.value
    TEAM_TELECOM = UtilityRUS.TEAM_TELECOM_RUS.value + UtilityIcon.HANDSET.value
    U_COM = UtilityRUS.U_COM_RUS.value + UtilityIcon.INTERNET.value
    OVIO = UtilityRUS.OVIO_RUS.value + UtilityIcon.TV.value
