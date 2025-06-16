import json
import random

import aiohttp
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from core.cache_settings import redis_client
from core.exceptions import (
    ApiError,
    ApiProxyListError,
    ApiResponseDataError,
    ApiResponseStatusError,
    JsonError,
    ProxyList404, ApiRateLimitedError,
)
from core.logger_settings import logger
from services.enums import TTL, ProxyMessage, StatusType, WebshareProxy, ProxySettings


async def get_proxy_list(
        url: str,
        headers: dict,
        params: dict,
        required_key: str,
) -> list:
    """Асинхронно запрашивает список прокси (или другие данные) с API.
    Выполняет GET-запрос по переданному URL с указанными headers и params.
    Проверяет статус ответа, парсит ответ как JSON, валидирует, что это словарь.
    Возвращает значение по ключу required_key из ответа.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=url,
                    headers=headers,
                    params=params,
            ) as response:
                if response.status == 429:
                    error_message = ProxyMessage.API_RATE_LIMITED.value
                    logger.error(error_message)
                    raise ApiRateLimitedError(error_message)
                elif response.status != 200:
                    error_message = ProxyMessage.API_RESPONSE_ERROR.value.format(
                        response_status=response.status,
                        text=await response.text(),
                    )
                    logger.error(error_message)
                    raise ApiResponseStatusError(error_message)
                data = await response.json()
                if not isinstance(data, dict):
                    error_message = ProxyMessage.BAD_RESPONSE.value.format(
                        data=data
                    )
                    logger.error(error_message)
                    raise ApiResponseDataError(error_message)
                return data.get(required_key)
    except Exception as e:
        error_message = ProxyMessage.API_ERROR.value.format(e=e)
        logger.error(error_message)
        raise ApiError(error_message)


@retry(
    retry=retry_if_exception_type((
        ApiResponseStatusError,
        ApiRateLimitedError,
    )),
    stop=stop_after_attempt(3),
    sleep=ProxySettings.RETRY_TIMEOUT_PROXY_LIST.value,
)
async def get_proxy_list_with_retry() -> list:
    return await get_proxy_list(
        url=WebshareProxy.URL_LIST.value,
        headers=WebshareProxy.HEADERS.value,
        params=WebshareProxy.PARAMS_URL_LIST.value,
        required_key=WebshareProxy.RESULT_KEY.value,
    )


async def add_proxy_list_in_cash(
        proxy_list: list[dict],
        proxy_list_name: str,
) -> None:
    """Добавляет список прокси в кэш Redis с TTL.
    Всем элементам проставляет статус OK и обнуляет failures.
    """
    # todo где то тут добавить значение для уже запрашиваемого листа прокси,
    # todo чтобы не делать несколько запросов подряд() может флаг(processing)?
    # todo добавить допустим словарь с ключом в "процессе", чтобы не ломать логику ниже

    for proxy in proxy_list:
        proxy['status'] = StatusType.OK.value
        proxy['failures'] = 0
    try:
        await redis_client.set(
            proxy_list_name,
            json.dumps(proxy_list),
            ex=TTL.PROXY_LIST.value,
        )
    except Exception as e:
        logger.error(ProxyMessage.PROXY_LIST_ADD_ERROR.value.format(
            error=str(e),
        ))
    else:
        logger.info(ProxyMessage.PROXY_LIST_OK.value)


async def get_random_proxy_from_cash(key: str) -> dict:
    """Возвращает случайный валидный прокси из кэша Redis по заданному ключу.
    Фильтрует по статусу OK и valid=True.
    """
    raw_data = await redis_client.get(key)
    if not raw_data:
        raise ProxyList404(ProxyMessage.LIST_NOT_FOUND.value)
    list_data = json.loads(raw_data)
    if not list_data:
        raise JsonError(ProxyMessage.EMPTY_KEY.value)
    valid_proxies = [
        proxy for proxy in list_data
        if proxy.get('status') == StatusType.OK.value
           and proxy.get('valid') is True
           and proxy.get('failures') < 1
    ]
    if not valid_proxies:
        raise ApiProxyListError(
            ProxyMessage.PROXY_LIST_VALID_ERROR.value.format(
                proxy_list=list_data[:50],
            ),
        )
    return random.choice(valid_proxies)

# async def main():
#     proxy_list = await get_proxy_list_with_retry()
#     await add_proxy_list_in_cash(proxy_list, WebshareProxy.LIST_NAME.value)
#     print(proxy_list)
#     return await get_random_proxy_from_cash(WebshareProxy.LIST_NAME.value)
#
#
# pprint(asyncio.run(main()))
