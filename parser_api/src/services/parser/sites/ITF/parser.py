import random

from playwright.async_api import TimeoutError

from core.exceptions import Account404, Selector404
from core.logger_settings import logger
from services.enums import UtilityModelName
from services.parser.base import InitParser
from services.parser.sites.ITF.UI_text import (
    ITFDataElectricityNameSelector,
    ITFDataGasNameSelector,
    ITFDataWaterNameSelector,
    ITFFormTextAreaName,
    ITFGasFormClassSelect,
    ITFSiteButton,
)

ITF_FLAG = 'itf'


class ParserITF(InitParser):
    """Логика парсера ITF."""

    async def get_data(self):
        mapping = {
            UtilityModelName.GAS.value: lambda: self.parse_gas(),
            UtilityModelName.WATER.value: lambda: self.parse_water(),
            UtilityModelName.ELECTRICITY.value: lambda: self.parse_electricity(),
        }
        return await mapping.get(self.utility)()

    async def try_wait_for_selector(self, selector: str) -> bool:
        try:
            await self.page.wait_for_selector(
                selector,
                timeout=self.check_timeout,
            )
            return True
        except TimeoutError:
            return False

    async def raise_if_account_not_found(self):
        selectors = [
            '#message.alert-danger',
            '#message.alert.alert-danger',
            '#message.alert-danger.alert-dismissible',
        ]
        for sel in selectors:
            if await self.try_wait_for_selector(sel):
                logger.info(f'Счёт ({self.account}) не найден.')
                raise Account404

    @staticmethod
    async def get_result_data(selector_type: str, page_elements: list) -> dict:
        result_dict = {}
        mapping = {
            'gas': ITFDataGasNameSelector,
            'electricity': ITFDataElectricityNameSelector,
            'water': ITFDataWaterNameSelector,
        }
        mapping_enum = mapping.get(selector_type)
        for el in page_elements:
            p_tag = await el.query_selector('p.text-black')
            if not p_tag:
                continue
            p_text = (await p_tag.text_content()).strip()
            h6_tag_name = 'h6.hint-text'
            for selector in mapping_enum:
                if p_text == selector.value:
                    h6_tag = await el.query_selector(h6_tag_name)
                    result_dict[selector.name.lower()] = (
                        await h6_tag.text_content()
                        if h6_tag else None
                    ).strip()
        return result_dict

    async def parse_gas(self):
        await self.page.type(
            f'[name="{ITFFormTextAreaName.CUSTOMER_ID.value}"]',
            self.account,
            delay=random.randint(50, 100),
        )
        await self.page.click(
            f'[class="{ITFGasFormClassSelect.SELECT_CITY_LIST.value}"]',
        )
        await self.page.type(
            'input.select2-search__field',
            self.city or '',
            delay=random.randint(50, 100),
        )
        try:
            await self.page.locator(
                'li.select2-results__option.select2-results__option--highlighted',
            ).click()
        except self.playwright_errors as e:
            error = (f'({e.__class__.__name__}) '
                     f'Не найден селектор в выпадающем списке: {str(e)}')
            logger.error(error)
            raise Selector404
        await self.page.click(f'[class="{ITFSiteButton.SEARCH_BTN.value}"]')
        await self.raise_if_account_not_found()

        try:
            await self.page.wait_for_selector('#resultcard', timeout=5_000)
            elem = await self.page.query_selector('#resultcard')
            class_attr = await elem.get_attribute('class')
            if 'hide' in class_attr:
                raise Selector404(
                    'Элемент #resultcard скрыт, результат не выведен.',
                )
            page_elements = await self.page.query_selector_all('div.col-md-4')
        except self.playwright_errors as e:
            error = f'({e.__class__.__name__}): {str(e)}'
            logger.error(error)
            raise Selector404

        parsing_data = await self.get_result_data('gas', page_elements)
        address = parsing_data.get('address')
        consumption = parsing_data.get('consumption')
        debit_consumption = parsing_data.get('debit_consumption')
        debit_service = parsing_data.get('debit_service')
        debit_full = parsing_data.get('debit_full')

        logger.info(
            f'Результат парсинга: address ({address or None}), '
            f'consumption ({consumption}), '
            f'debit_consumption ({debit_consumption}), '
            f'debit_service ({debit_service}), '
            f'debit_full ({debit_full})',
        )
        return dict(
            address=address,
            consumption=consumption,
            debit_consumption=debit_consumption,
            debit_service=debit_service,
            debit_full=debit_full,
        )

    async def parse_water(self):

        await self.page.type(
            f'[name="{ITFFormTextAreaName.AGREEMENT.value}"]',
            self.account,
            delay=random.randint(50, 100),
        )
        await self.page.click(
            f'[class="{ITFSiteButton.SEARCH_BTN.value}"]',
        )
        await self.raise_if_account_not_found()
        try:
            await self.page.wait_for_selector('#result', timeout=6_000)
            page_elements = await self.page.query_selector_all('div.col-md-4')
        except self.playwright_errors as e:
            error = f'({e.__class__.__name__})'
            logger.error(error)
            raise Selector404

        parsing_data = await self.get_result_data('water', page_elements)
        address = parsing_data.get('address')
        consumption = parsing_data.get('consumption')
        debit_full = parsing_data.get('debit_full')

        logger.info(
            f'Результат парсинга: address ({address or None}), '
            f'consumption ({consumption}), '
            f'debit_full ({debit_full})',
        )
        return dict(
            address=address,
            consumption=consumption,
            debit_full=debit_full,
        )

    async def parse_electricity(self):
        await self.page.type(
            f'[name="{ITFFormTextAreaName.CUSTOMER_ID.value}"]',
            self.account,
            delay=random.randint(50, 100),
        )
        await self.page.click(
            f'[class="{ITFSiteButton.SEARCH_BTN.value}"]',
        )
        await self.raise_if_account_not_found()

        try:
            await self.page.wait_for_selector('#resultcard', timeout=5000)
            page_elements = await self.page.query_selector_all('div.col-md-4')
        except self.playwright_errors as e:
            error = f'({e.__class__.__name__})'
            logger.error(error)
            raise Selector404

        parsing_data = await self.get_result_data('electricity', page_elements)
        address = parsing_data.get('address')
        consumption = parsing_data.get('consumption')
        debit_full = parsing_data.get('debit_full')

        logger.info(
            f'Результат парсинга: address ({address or None}), '
            f'consumption ({consumption}), '
            f'debit_full ({debit_full})',
        )
        return dict(
            address=address,
            consumption=consumption,
            debit_full=debit_full,
        )
