from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from Auth.AuthHandler import AuthHandler
from Controller.User import auth_handler, user

app = FastAPI()
app.include_router(user, prefix="/api")
