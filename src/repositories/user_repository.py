from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.models import User
from src.db.models.telegram_contacts import TelegramContacts
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def get_by_telegram(self, username: str):
        query = select(self.model).options(selectinload(self.model.telegram_contact))
        result = self.db.execute(query)
        return result.scalar_one()
