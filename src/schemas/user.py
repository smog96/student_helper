from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class User(UserBase):
    id: int
