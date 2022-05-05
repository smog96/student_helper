from sqlalchemy.orm import joinedload
from sqlalchemy import select
from src.db.models import User
from src.db.models.telegram_contacts import TelegramContacts
from src.repositories.base import BaseRepository
from src.repositories.user_repository import UserRepository
from src.schemas.user import TelegramContactBase, TelegramUser, UserBase


class TelegramRepository(BaseRepository):
    """
    `tid` - telegram id
    """

    model = TelegramContacts

    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()

    def _find_user_by_tid(self, tid: int) -> TelegramUser:
        query = select(User).join(self.model).filter(self.model.telegram_id == tid)
        return self.return_scalar_one_(query, True)

    def set_telegram_for_user(self, telegram_user: TelegramUser):
        user = self._find_user_by_tid(tid=telegram_user.telegram_id)
        if user is None:
            user = UserBase(fio=telegram_user.fio)
