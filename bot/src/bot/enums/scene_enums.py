from enum import Enum

from bot.enums.utility_enums import UtilityName, UtilityNameIcon


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
            SceneName.ELECTRICITY.editor: UtilityNameIcon.ELECTRICITY,
            SceneName.GAS.editor: UtilityNameIcon.GAS,
            SceneName.GAS_SERVICE.editor: UtilityNameIcon.GAS_SERVICE,
            SceneName.WATER.editor: UtilityNameIcon.WATER,
            SceneName.VIVA_MTS.editor: UtilityNameIcon.VIVA_MTS,
            SceneName.TEAM_TELECOM.editor: UtilityNameIcon.TEAM_TELECOM,
            SceneName.U_COM.editor: UtilityNameIcon.U_COM,
            SceneName.OVIO.editor: UtilityNameIcon.OVIO,
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
            SceneName.ELECTRICITY.editor: UtilityName.ELECTRICITY.value,
            SceneName.GAS.editor: UtilityName.GAS.value,
            SceneName.GAS_SERVICE.editor: UtilityName.GAS_SERVICE.value,
            SceneName.WATER.editor: UtilityName.WATER.value,
            SceneName.VIVA_MTS.editor: UtilityName.VIVA_MTS.value,
            SceneName.TEAM_TELECOM.editor: UtilityName.TEAM_TELECOM.value,
            SceneName.U_COM.editor: UtilityName.U_COM.value,
            SceneName.OVIO.editor: UtilityName.OVIO.value,
        }
        return mapping.get(current_state)
