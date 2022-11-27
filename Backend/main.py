from fastapi import FastAPI

from Controller.UserController import user
from Controller.PersonController import person

app = FastAPI()
app.include_router(user, prefix="/api/user")
app.include_router(person, prefix="/api/person")
