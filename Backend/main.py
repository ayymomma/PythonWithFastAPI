from fastapi import FastAPI

from Controller.DocumentController import document
from Controller.UserController import user
from Controller.PersonController import person
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user, prefix="/api/user")
app.include_router(person, prefix="/api/person")
app.include_router(document, prefix="/api/document")
