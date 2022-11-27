from fastapi import Depends, APIRouter
from Service.UserService import create_user, login

user = APIRouter()


# register a new user
@user.post("/register", status_code=201)
def register(return_value: dict = Depends(create_user)):
    return return_value


# login
@user.post("/login")
def login(return_value: dict = Depends(login)):
    return return_value

