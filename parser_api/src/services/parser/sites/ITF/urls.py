from enum import Enum

from core.exceptions import ITFUrl404
from services.enums import UtilityModelName


class ITFUrl(str, Enum):
    GAS = 'https://itfllc.am/ru/payments/pay/gazprom-armenia-sparoxakan-partq'
    WATER = 'https://itfllc.am/hy/payments/pay/veolia-itf'
    ELECTRICITY = 'https://itfllc.am/ru/payments/pay/ena-phone-number'

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
