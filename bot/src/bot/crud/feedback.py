from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.crud.user import user_crud
from db.models.models import Feedback, UserProfile


class CRUDFeedback(CRUDBase):
    async def save_feedback(
            self,
            session: AsyncSession,
            telegram_id: str,
            feedback_type: str,
            feedback_text: str,
            feedback_status: str = None,
    ) -> Feedback:
        """Сохраняет отзыв пользователя."""
        user: UserProfile = user_crud.get_user_by_tg_id(session, telegram_id)
        return self.create(
            session,
            dict(
                user_id=str(user.id),
                feedback_type=feedback_type,
                text=feedback_text,
                status=feedback_status or 'new',
            ),
        )


feedback_crud = CRUDFeedback(Feedback)
