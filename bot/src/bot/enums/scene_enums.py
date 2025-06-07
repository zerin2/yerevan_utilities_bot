from enum import Enum


class FeedbackType(str, Enum):
    REVIEW = 'review'
    ERROR = 'error'


class UtilityModelName(str, Enum):
    ELECTRICITY = 'electricity'
    GAS = 'gas'
    GAS_SERVICE = 'gas_service'
    WATER = 'water'
    VIVA_MTS = 'viva_mts'
    TEAM_TELECOM = 'team_telecom'
    U_COM = 'u_com'
    OVIO = 'ovio'


class UtilityIcon(str, Enum):
    LIGHTNING = '⚡'
    FIRE = '🔥'
    TOOLS = '🛠️'
    DROP = '💧'
    PHONE = '📱'
    HANDSET = '📞'
    INTERNET = '🌐'
    TV = '📺'


class UtilityRUS(str, Enum):
    ELECTRICITY_RUS = ' Электричество '
    GAS_RUS = ' Газ '
    GAS_SERVICE_RUS = ' Газ (обслуживание) '
    WATER_RUS = ' Вода '
    VIVA_MTS_RUS = ' VIVA (MTS) '
    TEAM_TELECOM_RUS = 'team (Telecom Armenia) '
    U_COM_RUS = ' U! com '
    OVIO_RUS = ' OVIO | Rostelecom '


class Utility(Enum):
    ELECTRICITY = UtilityRUS.ELECTRICITY_RUS.value + UtilityIcon.LIGHTNING.value
    GAS = UtilityRUS.GAS_RUS.value + UtilityIcon.FIRE.value
    GAS_SERVICE = UtilityRUS.GAS_SERVICE_RUS.value + UtilityIcon.TOOLS.value
    WATER = UtilityRUS.WATER_RUS.value + UtilityIcon.DROP.value
    VIVA_MTS = UtilityRUS.VIVA_MTS_RUS.value + UtilityIcon.PHONE.value
    TEAM_TELECOM = UtilityRUS.TEAM_TELECOM_RUS.value + UtilityIcon.HANDSET.value
    U_COM = UtilityRUS.U_COM_RUS.value + UtilityIcon.INTERNET.value
    OVIO = UtilityRUS.OVIO_RUS.value + UtilityIcon.TV.value


class SceneName(Enum):
    START_MSG = 'start_msg_scene'
    LIST_UTILITIES = 'list_utilities_scene'
    REQUEST_READING = 'request_reading_scene'

    NOTICE_INTERVAL = 'notice_interval_scene'
    NOTICE_STATE = 'notice_state_scene'
    DATA = 'data_scene'

    ELECTRICITY = 'electricity_scene'
    GAS = 'gas_scene'
    GAS_SERVICE = 'gas_service_scene'
    WATER = 'water_scene'
    VIVA_MTS = 'viva_mts_scene'
    TEAM_TELECOM = 'team_telecom_scene'
    U_COM = 'u_com_scene'
    OVIO = 'ovio_scene'

    SETTING = 'setting_scene'
    FEEDBACK = 'feedback_scene'
    USUAL_REVIEW = 'usual_review_scene'
    FOUND_ERROR = 'found_error_scene'

    @property
    def display(self):
        return f'display_{self.value}'

    @property
    def editor(self):
        return f'editor_{self.value}'

    @property
    def check(self):
        return f'check_{self.value}'

    @property
    def save(self):
        return f'save_{self.value}'

    @property
    def get(self):
        return f'get_{self.value}'

    @staticmethod
    def to_utility_description(current_state: str) -> str:
        """Возвращает описание услуги (Utility) на основе текущего состояния FSM.
        Сопоставляет переданное состояние FSM с соответствующей услугой,
        используя предопределенный словарь сопоставлений.
        Пример:
            Если `current_state` равно 'add_electricity_scene',
            метод вернет `Utility.ELECTRICITY`.
        Параметры:
            current_state (str): Текущее состояние FSM пользователя,
            переданное как строка.
        Возвращает:
        str: Описание услуги (например, "Электричество"),
             если найдено соответствие. Если состояние не сопоставлено,
             возвращает None.

        """
        mapping = {
            SceneName.ELECTRICITY.editor: Utility.ELECTRICITY,
            SceneName.GAS.editor: Utility.GAS,
            SceneName.GAS_SERVICE.editor: Utility.GAS_SERVICE,
            SceneName.WATER.editor: Utility.WATER,
            SceneName.VIVA_MTS.editor: Utility.VIVA_MTS,
            SceneName.TEAM_TELECOM.editor: Utility.TEAM_TELECOM,
            SceneName.U_COM.editor: Utility.U_COM,
            SceneName.OVIO.editor: Utility.OVIO,
        }
        return mapping.get(current_state)

    @staticmethod
    def to_save(current_state: str) -> str:
        """Сопоставление состояния со SceneName."""
        mapping = {
            SceneName.ELECTRICITY.editor: SceneName.ELECTRICITY,
            SceneName.GAS.editor: SceneName.GAS,
            SceneName.GAS_SERVICE.editor: SceneName.GAS_SERVICE,
            SceneName.WATER.editor: SceneName.WATER,
            SceneName.VIVA_MTS.editor: SceneName.VIVA_MTS,
            SceneName.TEAM_TELECOM.editor: SceneName.TEAM_TELECOM,
            SceneName.U_COM.editor: SceneName.U_COM,
            SceneName.OVIO.editor: SceneName.OVIO,
        }
        return mapping.get(current_state)

    @staticmethod
    def to_utility_name(current_state: str) -> str:
        """Сопоставление состояния с UtilityModelName."""
        mapping = {
            SceneName.ELECTRICITY.editor: UtilityModelName.ELECTRICITY.value,
            SceneName.GAS.editor: UtilityModelName.GAS.value,
            SceneName.GAS_SERVICE.editor: UtilityModelName.GAS_SERVICE.value,
            SceneName.WATER.editor: UtilityModelName.WATER.value,
            SceneName.VIVA_MTS.editor: UtilityModelName.VIVA_MTS.value,
            SceneName.TEAM_TELECOM.editor: UtilityModelName.TEAM_TELECOM.value,
            SceneName.U_COM.editor: UtilityModelName.U_COM.value,
            SceneName.OVIO.editor: UtilityModelName.OVIO.value,
        }
        return mapping.get(current_state)
