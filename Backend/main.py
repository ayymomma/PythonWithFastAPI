from fastapi import FastAPI

from Controller.UserController import user

app = FastAPI()
app.include_router(user, prefix="/api")
