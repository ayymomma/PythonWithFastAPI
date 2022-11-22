from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import DataBase.Models as models
from Auth.AuthHandler import AuthHandler
from DDO.UserDDO import UserRegisterDDO, UserLoginDDO
from Service.UserService import get_db, username_exists, email_exists, create_user, login

user = APIRouter()


# register a new user
@user.post("/register", status_code=201)
def register(return_value: dict = Depends(create_user)):
    return return_value


# login
@user.post("/login")
def login(return_value: dict = Depends(login)):
    return return_value

