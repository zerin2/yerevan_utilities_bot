class ParserError(Exception):
    pass


class Selector404(ParserError):
    def __init__(self, message='Не найден селектор'):
        super().__init__(message)


class ModalCard404(ParserError):
    def __init__(self, message='Не найден модальное окно'):
        super().__init__(message)


class Page404(ParserError):
    def __init__(self, message='Не найдена страница'):
        super().__init__(message)


class Account404(ParserError):
    def __init__(self, message='Аккаунт не найден'):
        super().__init__(message)


class AccountData404(ParserError):
    def __init__(self, message='Нет данных аккаунта'):
        super().__init__(message)


class ValidationError(Exception):
    pass


class JsonError(ValidationError):
    pass


class EmptyKeyError(ValidationError):
    pass


class StatusError(Exception):
    pass

