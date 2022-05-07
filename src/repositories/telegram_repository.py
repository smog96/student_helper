from sqlalchemy.orm import joinedload
from sqlalchemy import select
from src.db.models.telegram_contacts import Telegram
from src.repositories.base import BaseRepository
from src.repositories.user_repository import UserRepository
from src.schemas.telegram_user import TelegramCreate


class TelegramRepository(BaseRepository):
    """
    `tid` - telegram id
    """

    model = Telegram

    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()

    def check_exist(self, tg_user):
        return bool(self.get(tg_id=tg_user.id))

    def create_(self, tg_user):
        user = self.user_repo.create_user()
        tg_instance = TelegramCreate(
            user_id=user.id,
            telegram_id=tg_user.id,
            username=tg_user.username
        )
        tg_data = self.create(instance=tg_instance)
        return tg_data

    def get(self, tg_id: int = None, **filters):
        query = select(self.model) \
            .options(joinedload(self.model.user)) \
            .where(self.model.telegram_id == tg_id)

        return self.return_scalar_one_(query)
