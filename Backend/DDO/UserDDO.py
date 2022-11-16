from pydantic import BaseModel, Field


class UserDDO(BaseModel):
    user_id: int
    username: str
    password: str
    email: str


class UserLoginDDO(BaseModel):
    username: str
    password: str


class UserRegisterDDO(BaseModel):
    user_id: int
    username: str
    password: str
    email: str
