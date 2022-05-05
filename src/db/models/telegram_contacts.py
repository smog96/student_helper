from enum import unique
from src.db.base_model import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class TelegramContacts(Base):
    __tablename__ = "telegram_contacts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="telegram_contact")

    username = Column(String, nullable=False, unique=True)
    telegram_id = Column(Integer, unique=True)
