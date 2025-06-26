from bot.crud.base import CRUDBase
from db.models.models import UserProfile


class CRUDUser(CRUDBase):
    pass




user_crud = CRUDUser(UserProfile)