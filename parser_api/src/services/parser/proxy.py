import asyncio
import random

import aiohttp

from core.settings import settings

WEBSHARE_TOKEN = settings.webshare_token
WEBSHARE_URL_LIST = 'https://proxy.webshare.io/api/v2/proxy/list/'
WEBSHARE_PARAMS_URL_LIST = {'mode': 'direct'}
WEBSHARE_HEADERS = {'Authorization': 'Token ' + WEBSHARE_TOKEN}

async def get_proxy_list() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=WEBSHARE_URL_LIST,
                headers=WEBSHARE_HEADERS,
                params=WEBSHARE_PARAMS_URL_LIST
        ) as response:
            data = await response.json()
            return data['results']



# 'http': 'http://user123:pass456@1.2.3.4:8080',
# http://username:password@proxy_address:port

# 'username': 'jqsjwunw',
# 'password': 'hd9wm3292a73',
# 'proxy_address':
# '198.23.239.134',
# 'port': 6540

# f'http://{username}:{password}@{proxy_address}:{port}'

asyncio.run(get_proxy_list())
