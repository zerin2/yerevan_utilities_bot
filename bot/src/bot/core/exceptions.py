class CustomBaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __repr__(self):
        return f'({self.__class__.__name__}): {self.message}'

    def __str__(self):
        return self.__repr__()


class StartNoticeInterval404(CustomBaseException):
    """Исключение: не найдено время начала интервала оповещений."""


class EndNoticeInterval404(CustomBaseException):
    """Исключение: не найдено время окончания интервала оповещений."""


class NoticeType404(CustomBaseException):
    """Исключение: не найден тип оповещения."""


class ParserError(CustomBaseException):
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


class ValidationError(CustomBaseException):
    pass
