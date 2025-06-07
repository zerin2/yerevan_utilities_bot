from exceptions import EmptyKeyError
from workers.config import CHECK_KEYS


def check_data_keys(data):
    for key in CHECK_KEYS:
        if not data.get(key):
            raise EmptyKeyError(f'Пустой ключ "{key}"')
