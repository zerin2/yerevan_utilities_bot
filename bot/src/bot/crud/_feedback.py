from bot.crud._base import BaseBotManager
from bot.crud._user import UserBotManager
from db.models import Feedback, UsersProfile


class FeedbackBotManger(BaseBotManager):
    """Менеджер для обработки отзывов пользователей в боте.

    Описание:
    ----------
    Класс предоставляет методы для работы с отзывами пользователей,
    включая их сохранение и управление.
    """

    async def save_feedback(
            self,
            tg_id: str,
            feedback_type: str,
            feedback_text: str,
            feedback_status: str = None,
    ) -> Feedback:
        """Сохраняет отзыв пользователя в базе данных.

        Параметры:
        ----------
        tg_id : str
            Telegram ID пользователя, оставившего отзыв.
        feedback_type : str
            Тип отзыва (например, 'review' или 'error').
        feedback_text : str
            Текст отзыва, оставленный пользователем.
        feedback_status : str, optional
            Статус отзыва (по умолчанию 'new').

        Возвращает:
        ----------
        Feedback
            Объект отзыва, созданный и сохранённый в базе данных.

        Исключения:
        -----------
        ValueError
            Если пользователь с указанным Telegram ID не найден.

        Описание:
        ---------
        1. Получает пользователя из базы данных по Telegram ID через `UserBotManager`.
        2. Создаёт новый отзыв, привязывая его к идентификатору пользователя.
        3. Сохраняет отзыв в базе данных со статусом 'new', если статус не указан.
        4. Возвращает объект созданного отзыва.
        """
        user_repo = UserBotManager(self.session)
        user: UsersProfile = await user_repo.get_user_by_tg_id(str(tg_id))
        user_feedback = await self.add_new_instance(
            self.FEEDBACK_MODEL,
            {
                'user_id': str(user.id),
                'type': feedback_type,
                'text': feedback_text,
                'status': feedback_status or 'new',
            },
        )
        return user_feedback
