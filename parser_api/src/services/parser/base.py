import asyncio
import json
import random
from dataclasses import dataclass

import aiofiles
from playwright.async_api import BrowserContext, Error, Page, TimeoutError

import services.parser.config as conf
from core.exceptions import ParserError
from core.logger_settings import logger


@dataclass
class InitParser:
    message_data: dict
    account: str = None
    account_type: str = None
    utility: str = None
    city: str = None
    proxy: dict = None
    viewport: list[dict] = None
    headless_config: bool = None
    context: BrowserContext = None
    page: Page = None
    block_resource: list = None
    check_timeout: bool = conf.USUAL_CHECK_TIMEOUT
    playwright_errors: tuple = (Error, TimeoutError, Exception)

    def __post_init__(self):
        self.account = self.message_data.get('account')
        self.city = self.message_data.get('city')
        self.account_type = self.message_data.get('account_type')
        self.utility = self.message_data.get('utility')
        self.viewport = random.choice(conf.BROWSER_VIEWPORT)
        self.block_resource = conf.BLOCK_BROWSER_RESOURCES
        self.headless_config = True  # todo убрать в проде
        # self.headless_config = False if settings.debug else True
        if self.message_data.get('first_check'):
            self.check_timeout = conf.FIRST_CHECK_TIMEOUT

    @staticmethod
    async def get_random_user_agent():
        """Читаем файл 'user_agent.json' и выбираем рандомный юзер агент."""
        async with aiofiles.open(
                conf.USER_AGENT_PATH,
                mode='r',
                encoding='utf-8',
        ) as file:
            content = await file.read()
            return random.choice(json.loads(content))

    async def random_move_mouse(self):
        """Рандомное поведение мышки с небольшой задержкой."""
        await self.page.mouse.move(random.randint(50, 100), random.randint(50, 100))
        await asyncio.sleep(random.uniform(0.2, 0.5))

    @staticmethod
    def random_init_script():
        """Задаем рандомные данные в строку скрипта для браузера, данные в config."""
        script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => !webdriver!});
        Object.defineProperty(navigator, 'plugins', {get: () => !plugins!});
        Object.defineProperty(navigator, 'languages', {get: () => !languages!});
        """
        return (
            script.replace(
                '!webdriver!', random.choice(conf.WEBDRIVER),
            ).replace(
                '!plugins!', str(conf.PLUGINS[:random.randint(1, len(conf.PLUGINS))]),
            ).replace(
                '!languages!', str(random.sample(conf.LANGUAGES, k=2)),
            )
        )

    async def block_resources(self, route, request):
        """Блокирует загрузку определённых типов ресурсов на странице.
        Если тип ресурса (например, 'image', 'stylesheet', 'font') содержится
        в self.block_resource, то запрос будет отменён (abort), иначе продолжен.
        """
        if request.resource_type in self.block_resource:
            await route.abort()
        else:
            await route.continue_()

    async def init_header(self, browser):
        """Инициализирует новый браузерный контекст со случайным user-agent
        и параметрами прокси/размера экрана.
        Создаёт контекст с кастомным user-agent, размером окна
        и прокси (если указан).
        Добавляет скрипт для инициализации
        и роутинг для блокировки лишних ресурсов.
        В случае ошибки логирует её и выбрасывает ParserError.
        """
        try:
            user_agent = await self.get_random_user_agent()
            self.context = await browser.new_context(
                user_agent=user_agent,
                viewport=self.viewport,
                proxy=self.proxy,
            )
            await self.context.route('**/*', self.block_resources)
            await self.context.add_init_script(self.random_init_script())
        except self.playwright_errors as e:
            error_message = f'Ошибка при формировании контекста с заголовками: {str(e)}'
            logger.error(error_message)
            raise ParserError(error_message)
        else:
            logger.info(
                f'Запущен парсер с параметрами: '
                f'user_agent={user_agent}, '
                f'viewport={self.viewport}, '
                f'proxy={self.proxy.get('server') if self.proxy else None}',
            )
