import re
from enum import Enum

from playwright.async_api import async_playwright
from tenacity import (
    RetryError,
    retry,
    stop_after_attempt,
)

from core.exceptions import (
    ApiProcessingException,
    ApiProxyListError,
    PageError,
    ProxyList404,
    UrlFlagError,
)
from core.logger_settings import logger
from services.enums import ProxySettings, WebshareProxy
from services.parser.base import InitParser
from services.parser.proxy import (
    add_proxy_list_in_cash,
    create_empty_proxy_list_in_cash,
    get_api_proxy_list_with_retry,
    get_random_proxy_from_cash,
    increase_proxy_failures,
)
from services.parser.sites.ConverseBank.parser import (
    CONVERSE_BANK_FLAG,
    ParserConverseBank,
)
from services.parser.sites.ITF.parser import ITF_FLAG, ParserITF
from services.parser.sites.ITF.urls import ITFUrl


class Parser(InitParser):
    @staticmethod
    def get_map_urls(
            site_names: list[Enum],
            method: str,
            utility: str,
    ) -> list[str]:
        return list(map(lambda x: getattr(x, method)(utility), site_names))

    @retry(stop=stop_after_attempt(3))
    async def retry_goto(self, url):
        await self.page.goto(url)

    @staticmethod
    def detect_url_flag(url: str) -> str | None:
        if re.search(r'itfllc', url):
            return ITF_FLAG
        if re.search(r'conversebank', url):
            return CONVERSE_BANK_FLAG
        raise UrlFlagError

    @staticmethod
    def get_parser(parser_type, data: dict):
        parser_class = PARSER_CLASSES.get(parser_type)
        if not parser_class:
            raise ValueError(f'Нет обработчика для типа {parser_type}')
        return parser_class(data)

    async def run(self):
        """Основная логика работы парсера."""
        urls = self.get_map_urls(
            [
                ITFUrl,  # тут добавляем новый сайт для парсинга
            ],
            'to_utility_url',
            self.utility,
        )
        for attempt in range(ProxySettings.PROXY_ATTEMPT.value):
            try:
                raw_proxy = await get_random_proxy_from_cash(
                    WebshareProxy.LIST_NAME.value,
                )
                proxy_address = raw_proxy.get('proxy_address')
                proxy_port = raw_proxy.get('port')
                proxy_id = raw_proxy.get('id')
                proxy_server = ProxySettings.PROXY_TEMPLATE.value.format(
                    proxy_address=proxy_address,
                    port=proxy_port,
                )
                logger.info(
                    f'Попытка №{attempt + 1} '
                    f'с прокси: {proxy_server}',
                )
            except ProxyList404 as e:
                logger.info(e.__class__.__name__)
                self.proxy = None
                await create_empty_proxy_list_in_cash(
                    WebshareProxy.LIST_NAME.value,
                )
                proxy_list = await get_api_proxy_list_with_retry()
                if proxy_list:
                    await add_proxy_list_in_cash(
                        proxy_list,
                        WebshareProxy.LIST_NAME.value,
                    )
            except (ApiProxyListError, ApiProcessingException) as e:
                logger.info(e.__class__.__name__)
                self.proxy = None
            else:
                self.proxy = {
                    'server': proxy_server,
                    'username': raw_proxy.get('username'),
                    'password': raw_proxy.get('password'),
                }

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless_config)
                try:
                    await self.init_header(browser)
                    self.page = await self.context.new_page()

                    for url in urls:
                        try:
                            await self.retry_goto(url)
                            logger.info(f'Успешный переход по: {url}')
                            break
                        except RetryError as e:
                            error_message = (
                                f'(Proxy: {self.proxy['server']}) '
                                f'Не удалось перейти по {url} '
                                f'после 3 попыток: {str(e)}',
                            )
                            logger.warning(error_message)
                            raise PageError(error_message)
                    try:
                        cookies = await self.context.cookies()
                        await self.context.add_cookies(cookies)
                    except self.playwright_errors as e:
                        logger.error(f'Ошибка получения cookies: {str(e)}')

                    parser = self.get_parser(
                        self.detect_url_flag(url),
                        self.message_data,
                    )
                    parser.context = self.context
                    parser.page = self.page
                    data = await parser.get_data()
                    await self.context.clear_cookies()
                    await browser.close()
                    logger.info('Парсер завершил работу.')
                    return data
                except PageError as e:
                    logger.warning(f'Ошибка PageError: {str(e)}')
                    await browser.close()
                    await increase_proxy_failures(
                        proxy_id=str(proxy_id),  # noqa
                        proxy_list_name=WebshareProxy.LIST_NAME.value,
                    )
                    logger.info(f'Счётчик ошибок прокси {proxy_id} увеличен.')
                    continue
        raise PageError('Не удалось выполнить парсинг ни с одним из прокси')


PARSER_CLASSES = {
    ITF_FLAG: ParserITF,
    CONVERSE_BANK_FLAG: ParserConverseBank,
}
