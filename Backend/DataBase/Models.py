from sqlalchemy import Column, Integer, String
from DataBase.Database import Base


class User(Base):
    __tablename__   = "user"
    user_id         = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True)
    password        = Column(String)
    email           = Column(String, unique=True, index=True)
