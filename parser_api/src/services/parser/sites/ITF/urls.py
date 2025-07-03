from enum import Enum

from core.exceptions import ITFUrl404
from core.settings import settings
from services.enums import UtilityModelName


class ITFUrl(str, Enum):
    GAS = settings.itf_url_gas
    WATER = settings.itf_url_water
    ELECTRICITY = settings.itf_url_electricity

    @staticmethod
    def to_utility_url(utility: str) -> str:
        name = UtilityModelName
        mapping = {
            name.ELECTRICITY.value: ITFUrl.ELECTRICITY.value,
            name.GAS.value: ITFUrl.GAS.value,
            name.WATER.value: ITFUrl.WATER.value,
        }
        utility_url = mapping.get(utility)
        if utility_url is not None:
            return utility_url
        raise ITFUrl404(value=utility)
