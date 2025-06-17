class CustomBaseException(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f'({self.__class__.__name__}): {self.message}'

    def __str__(self):
        return self.__repr__()


class ParserError(CustomBaseException):
    def __init__(self, message='Ошибка парсера PLAYWRITE'):
        super().__init__(message)


class ITFUrl404(CustomBaseException):
    def __init__(
            self,
            value: str = None,
            message: str = 'Не найден ITF_url под тип аккаунта',
    ):
        self.value = value
        full_message = f'{message}: {value}' if value is not None else message
        super().__init__(full_message)


class ConverseBankUrl404(CustomBaseException):
    def __init__(
            self,
            value: str = None,
            message: str = 'Не найден ConverseBank_url под тип аккаунта',
    ):
        self.value = value
        full_message = f'{message}: {value}' if value is not None else message
        super().__init__(full_message)


class UrlFlagError(CustomBaseException):
    def __init__(self, message='Не сработал флаг урл'):
        super().__init__(message)


class Selector404(CustomBaseException):
    def __init__(self, message='Не найден селектор'):
        super().__init__(message)


class ModalCard404(CustomBaseException):
    def __init__(self, message='Не найден модальное окно'):
        super().__init__(message)


class PageError(CustomBaseException):
    def __init__(self, message='Не удалось открыть страницу'):
        super().__init__(message)


class Account404(CustomBaseException):
    def __init__(self, message='Аккаунт не найден'):
        super().__init__(message)


class AccountData404(CustomBaseException):
    def __init__(self, message='Нет данных аккаунта'):
        super().__init__(message)


class ValidationError(CustomBaseException):
    pass


class JsonError(CustomBaseException):
    pass


class StatusError(CustomBaseException):
    pass


class RedisTaskNotFound(CustomBaseException):
    def __init__(
            self,
            message='Задача с указанным task_id не найдена в Redis.',
    ):
        super().__init__(message)


class ProxyList404(CustomBaseException):
    pass


class ApiProcessingException(CustomBaseException):
    pass


class DuplicateAccountError(CustomBaseException):
    def __init__(
            self,
            message='Найдены дублирующиеся аккаунты.',
    ):
        super().__init__(message)


class ApiError(CustomBaseException):
    pass


class ApiResponseStatusError(CustomBaseException):
    pass


class ApiRateLimitedError(CustomBaseException):
    pass


class ApiResponseDataError(CustomBaseException):
    pass


class ApiProxyListError(CustomBaseException):
    pass
