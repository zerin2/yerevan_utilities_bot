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

    pass


class EndNoticeInterval404(CustomBaseException):
    """Исключение: не найдено время окончания интервала оповещений."""

    pass


class NoticeType404(CustomBaseException):
    """Исключение: не найден тип оповещения."""

    pass
