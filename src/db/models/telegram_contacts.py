from src.db.base_model import Base
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship


class Telegram(Base):
    __tablename__ = "telegram"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="telegram")

    username = Column(String, nullable=False, unique=True)
    telegram_id = Column(BigInteger, unique=True)
