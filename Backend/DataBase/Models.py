from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
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
    cnp = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))


class Receipt(Base):
    __tablename__ = "receipt"
    receipt_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(DateTime)
    amount = Column(Integer)
    person_id = Column(Integer, ForeignKey("person.person_id"))


class Document(Base):
    __tablename__ = "document"
    document_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    document_code = Column(String, unique=True)
    type = Column(String)
    expire_year = Column(Integer)


class Stats(Base):
    __tablename__ = "stats"
    stats_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    year = Column(Integer)
    amount = Column(Integer)
    persons = Column(Integer)
