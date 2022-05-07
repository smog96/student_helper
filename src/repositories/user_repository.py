from src.db.models import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def create_user(self):
        db_item = self.model()
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
