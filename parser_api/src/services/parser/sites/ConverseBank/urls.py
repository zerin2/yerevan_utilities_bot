from enum import Enum

from core.exceptions import ConverseBankUrl404
from services.enums import UtilityModelName


class ConverseBankUrl(str, Enum):
    GAS = 'https://portal.conversebank.am/ru/providers/check-balance?id=66'
    GAS_SERVICE = 'https://portal.conversebank.am/ru/providers/check-balance?id=67'
    WATER = 'https://portal.conversebank.am/ru/providers/check-balance?id=64'
    ELECTRICITY = 'https://portal.conversebank.am/ru/providers/check-balance?id=65'

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
