from core.settings import BASEDIR_PROJECT

USER_AGENT_FILE_NAME = 'user_agent.json'
USER_AGENT_PATH = BASEDIR_PROJECT / 'services/parser/data' / USER_AGENT_FILE_NAME

BROWSER_VIEWPORT = [{'width': 1280, 'height': 720}]
WEBDRIVER = ['undefined', 'null', 'false']
PLUGINS = [1, 2, 3, 4, 5]
BLOCK_BROWSER_RESOURCES = [
    'image',
    'font',
    'media',
]

FIRST_CHECK_TIMEOUT = 3500
USUAL_CHECK_TIMEOUT = 500

LANGUAGES = [
    'hy-AM',  # Армянский
    'ru-RU',  # Русский
    'en-US', 'en-GB',  # Английский
]
