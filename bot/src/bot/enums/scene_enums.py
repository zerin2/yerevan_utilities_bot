from enum import Enum

from bot.enums.utility_enums import UtilityLabel, UtilityName
from settings import AVAILABLE_UTILITIES


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
    def scene_editor_to_utility_label(value: str) -> str:
        """Возвращает по editor-сцене label услуги (иконка + русское название)."""
        mapping = {
            SceneName.ELECTRICITY.editor: UtilityLabel.ELECTRICITY,
            SceneName.GAS.editor: UtilityLabel.GAS,
            SceneName.GAS_SERVICE.editor: UtilityLabel.GAS_SERVICE,
            SceneName.WATER.editor: UtilityLabel.WATER,
            SceneName.VIVA_MTS.editor: UtilityLabel.VIVA_MTS,
            SceneName.TEAM_TELECOM.editor: UtilityLabel.TEAM_TELECOM,
            SceneName.U_COM.editor: UtilityLabel.U_COM,
            SceneName.OVIO.editor: UtilityLabel.OVIO,
        }
        return mapping.get(value)

    @staticmethod
    def editor_to_scene_enum(value: str) -> str:
        """Возвращает Enum-сцену (SceneName) по editor-сцене."""
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
        return mapping.get(value)

    @staticmethod
    def editor_to_utility_name(value: str) -> str:
        """Возвращает техническое имя услуги (UtilityName) по editor-сцене."""
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
        return mapping.get(value)


# Список доступных editor-сцен для утилит из AVAILABLE_UTILITIES
EDITOR_AVAILABLE_SCENE_NAMES = [
    getattr(SceneName, utility.name).editor
    for utility in UtilityName if utility in AVAILABLE_UTILITIES
]
