from fastapi import Depends
from sqlalchemy import extract
from sqlalchemy.orm import Session

from DDO.PersonDDO import PersonAddDDO
from DDO.ReceiptDDO import ReceiptAddDDO
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
    person_model = models.Person(first_name=person_add.first_name,
                                 last_name=person_add.last_name,
                                 phone=person_add.phone,
                                 area=person_add.area,
                                 quantity=person_add.quantity,
                                 cnp=person_add.cnp,
                                 user_id=user_id)
    db.add(person_model)
    db.commit()
    db.refresh(person_model)
    return {"message": "Person created"}


def get_person_by_cnp(cnp: str, db: Session = Depends(get_db),
                      user_id: int = Depends(auth_handler.auth_wrapper)):
    person_model = db.query(models.Person).filter(models.Person.user_id == user_id) \
        .filter(models.Person.cnp == cnp).first()
    if not person_model:
        return {"message": "Person not found"}
    return person_model


def get_person_by_name(first_name: str, last_name: str | None = None, db: Session = Depends(get_db),
                       user_id: int = Depends(auth_handler.auth_wrapper)):
    if last_name is None:
        person_model = db.query(models.Person).filter(models.Person.user_id == user_id) \
            .filter(models.Person.first_name == first_name).all()
    else:
        person_model = db.query(models.Person).filter(models.Person.user_id == user_id) \
            .filter(models.Person.first_name == first_name) \
            .filter(models.Person.last_name == last_name).all()

    if not person_model:
        return {"message": "Person not found"}
    return person_model


def get_person_by_page(page: int, no_per_page: int, db: Session = Depends(get_db),
                       user_id: int = Depends(auth_handler.auth_wrapper)):
    person_model = db.query(models.Person).filter(models.Person.user_id == user_id) \
        .offset(page * no_per_page).limit(no_per_page).all()
    if not person_model:
        return {"message": "Person not found"}
    return person_model


def add_receipt(receipt: ReceiptAddDDO, db: Session = Depends(get_db),
                user_id: int = Depends(auth_handler.auth_wrapper)):
    receipt_model = models.Receipt(name=receipt.name,
                                   date=receipt.date,
                                   amount=receipt.amount,
                                   person_id=receipt.person_id)
    db.add(receipt_model)
    db.commit()
    db.refresh(receipt_model)
    return {"message": "Receipt added"}


def get_receipt_by_person_id_and_year(person_id: int, year: int, db: Session = Depends(get_db),
                                      user_id: int = Depends(auth_handler.auth_wrapper)):
    receipt_model = db.query(models.Receipt).filter(models.Receipt.person_id == person_id) \
        .filter(extract("year", models.Receipt.date) == year).all()
    if not receipt_model:
        return []
    return receipt_model


def get_number_of_pages(no_per_page: int, db: Session = Depends(get_db),
                        user_id: int = Depends(auth_handler.auth_wrapper)):
    person_model = db.query(models.Person).filter(models.Person.user_id == user_id).all()
    # round at next integer
    return {"pages": -(-len(person_model) // no_per_page)}


def delete_person_by_id(person_id: int, db: Session = Depends(get_db),
                        user_id: int = Depends(auth_handler.auth_wrapper)):
    person_model = db.query(models.Person).filter(models.Person.user_id == user_id) \
        .filter(models.Person.person_id == person_id).first()
    if not person_model:
        return {"message": "Person not found"}
    db.delete(person_model)
    db.commit()
    return {"message": "Person deleted"}


def get_all_area(db: Session = Depends(get_db),
                 user_id: int = Depends(auth_handler.auth_wrapper)):
    person_model = db.query(models.Person).filter(models.Person.user_id == user_id).all()
    if not person_model:
        return {"message": "Person not found"}
    area = 0
    for person in person_model:
        area += person.area
    return {"area": round(area, 2)}
