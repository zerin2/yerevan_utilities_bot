import html
from dataclasses import dataclass

from aiogram.types import Message

from logs.config import bot_logger


@dataclass
class ValidateText:
    """Класс для проверки и обработки текста сообщения.
    Атрибуты:
    ----------
    message : Message
        Сообщение, полученное от пользователя.
    Методы:
    -------
    convert_html_symbol():
        Экранирует специальные HTML-символы в тексте сообщения для безопасности.
    async validate():
        Выполняет проверку длины текста и логирует сообщение.
        Если длина текста превышает 500 символов, отправляет уведомление пользователю.
    """

    message: Message

    def convert_html_symbol(self):
        """Экранирует специальные HTML-символы в тексте сообщения.

        Returns
        -------
        str
            Текст сообщения с экранированными HTML-символами.

        """
        return html.escape(self.message.text.lower())

    async def validate(self):
        """Валидирует текст сообщения.

        1. Экранирует HTML-символы.
        2. Логирует сообщение и информацию о пользователе.
        3. Проверяет длину сообщения:
           - Если длина превышает 500 символов, отправляет уведомление пользователю.
           - В противном случае возвращает экранированный текст.

        Returns
        -------
        str or None
            Экранированный текст сообщения, если оно валидно. Иначе None.

        """
        user_input = self.convert_html_symbol()
        bot_logger.info(f'Получено сообщение: "{self.message.text}" '
                        f'(экранировано: "{user_input}") '
                        f'от пользователя {self.message.from_user.id}')
        if len(user_input) > 500:
            await self.message.reply('Сообщение слишком длинное. '
                                     'Пожалуйста, сократите его до 500 символов.')
            return None
        return user_input
