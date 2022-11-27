from fastapi import Depends
from sqlalchemy.orm import Session

from DDO.PersonDDO import PersonSearchCNPDDO, PersonAddDDO
from DataBase.Database import SessionLocal
import DataBase.Models as models
from Service.UserService import auth_handler


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_person(person_add: PersonAddDDO, db: Session = Depends(get_db),
                  user_id: int = Depends(auth_handler.auth_wrapper)):
    if user_id:
        person_model = models.Person(first_name=person_add.first_name,
                                     last_name=person_add.last_name,
                                     phone=person_add.phone,
                                     area=person_add.area,
                                     quantity=person_add.quantity,
                                     cnp=person_add.cnp)
        db.add(person_model)
        db.commit()
        db.refresh(person_model)
        return {"message": "Person created"}

    return {"message": "Invalid credentials"}


def get_person_by_cnp(cnp: str, db: Session = Depends(get_db),
                      user_id: int = Depends(auth_handler.auth_wrapper)):
    person_model = db.query(models.Person).filter(models.Person.cnp == cnp).first()
    if not person_model:
        return {"message": "Person not found"}
    return person_model
