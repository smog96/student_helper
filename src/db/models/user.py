from src.db.base_model import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    telegram = relationship("Telegram", back_populates="user")
    # student_data = ...
