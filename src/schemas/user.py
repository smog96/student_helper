from pydantic import BaseModel


class UserBase(BaseModel):
    fio: str


class TelegramContactBase(BaseModel):
    user_id: int
    username: str
    telegram_id: str


class TelegramUser(UserBase):
    pass
