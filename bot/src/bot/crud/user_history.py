from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud.base import CRUDBase
from bot.crud.user import user_crud
from db.models.models import UserHistory, UserProfile


class CRUDUserHistory(CRUDBase):
    async def write_history(
            self,
            session: AsyncSession,
            message: Message,
            state: FSMContext | str = '',
    ) -> UserHistory | None:
        """Сохраняет действие пользователя."""
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.message_id
        message_content = message.text

        if isinstance(state, FSMContext):
            state = str(await state.get_data())
        user_obj: UserProfile = await user_crud.get_or_create_user(
            session, user_id,
        )
        return self.create(
            session,
            {
                'user_id': user_obj.id,
                'chat_id': chat_id,
                'message_id': message_id,
                'message_content': message_content,
                'state': state,
            },
        )


user_history_crud = CRUDUserHistory(UserHistory)
