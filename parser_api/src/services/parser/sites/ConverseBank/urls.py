from enum import Enum

from core.exceptions import ConverseBankUrl404
from core.settings import settings
from services.enums import UtilityModelName


class ConverseBankUrl(str, Enum):
    GAS = settings.converse_bank_url_gas
    GAS_SERVICE = settings.converse_bank_url_gas_service
    WATER = settings.converse_bank_url_water
    ELECTRICITY = settings.converse_bank_url_electricity

    @staticmethod
    def to_utility_url(utility: str) -> str:
        name = UtilityModelName
        mapping = {
            name.ELECTRICITY.value: ConverseBankUrl.ELECTRICITY.value,
            name.GAS.value: ConverseBankUrl.GAS.value,
            name.GAS_SERVICE.value: ConverseBankUrl.GAS_SERVICE.value,
            name.WATER.value: ConverseBankUrl.WATER.value,
        }
        utility_url = mapping.get(utility)
        if utility_url is not None:
            return utility_url
        raise ConverseBankUrl404(value=utility)
