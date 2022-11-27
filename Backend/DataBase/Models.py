from sqlalchemy import Column, Integer, String, ForeignKey, Float
from DataBase.Database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)


class Person(Base):
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    area = Column(Float)
    quantity = Column(Integer)
    cnp = Column(String, unique=True, index=True)


class Document(Base):
    __tablename__ = "document"
    document_id = Column(Integer, primary_key=True, index=True)
    document_code = Column(String, unique=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
