from pydantic.main import BaseModel

from src.schemas.user import User


class TelegramBase(BaseModel):
    telegram_id: int
    username: str


class Telegram(TelegramBase):
    user: User


class TelegramCreate(TelegramBase):
    user_id: int
