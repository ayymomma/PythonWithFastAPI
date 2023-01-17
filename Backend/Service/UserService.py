from fastapi import Depends
from sqlalchemy.orm import Session

from Auth.AuthHandler import AuthHandler
from DDO.UserDDO import UserRegisterDDO, UserLoginDDO
from DataBase.Database import SessionLocal
import DataBase.Models as models

from DataBase.Database import engine
models.Base.metadata.create_all(bind=engine)
auth_handler = AuthHandler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def username_exists(username: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username == username).first() is not None


def email_exists(email: str, user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email)\
               .filter(models.User.user_id != user_id).first() is not None


def create_user(user_register: UserRegisterDDO, db: Session = Depends(get_db)):
    if username_exists(user_register.username, db):
        return {"message": "Username already exists"}
    if email_exists(user_register.email, user_register.user_id, db):
        return {"message": "Email already exists"}
    user_model = models.User(username=user_register.username,
                             password=auth_handler.get_password_hash(user_register.password),
                             email=user_register.email)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "User created"}


def login(user_login: UserLoginDDO, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.username == user_login.username).first()
    if not user_model or not auth_handler.verify_password(user_login.password, user_model.password):
        return {"message": "Invalid credentials"}
    token = auth_handler.encode_token(user_model.user_id)
    return {"token": token}


def get_logs(user_id: int = Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    log_model = db.query(models.Log).filter(models.Log.user_id == user_id).all()
    if not log_model:
        return []
    return log_model
