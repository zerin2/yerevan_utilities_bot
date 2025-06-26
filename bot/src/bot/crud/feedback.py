from bot.crud.base import CRUDBase
from db.models.models import Feedback


class CRUDFeedback(CRUDBase):
    pass




feedback_crud = CRUDFeedback(Feedback)