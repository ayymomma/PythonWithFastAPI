from fastapi import FastAPI

from Controller.DocumentController import document
from Controller.UserController import user
from Controller.PersonController import person

app = FastAPI()
app.include_router(user, prefix="/api/user")
app.include_router(person, prefix="/api/person")
app.include_router(document, prefix="/api/document")
