from datetime import datetime

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

    stats_model = db.query(models.Stats).filter(models.Stats.user_id == user_id).first()
    stats_model.persons += 1
    stats_model.amount += person_add.area

    log_model = models.Log(user_id=user_id,
                           date=datetime.now(),
                           message=f"Added a new person with name {person_model.first_name} {person_model.last_name}"
                                   f" and area {person_model.area}")

    db.add(log_model)
    db.add(person_model)
    db.add(stats_model)
    db.commit()
    db.refresh(person_model)
    db.refresh(stats_model)
    db.refresh(log_model)
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
    person_model = db.query(models.Person).filter(models.Person.user_id == user_id)\
        .order_by(models.Person.first_name.asc()).order_by(models.Person.last_name.asc()) \
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
    # stats_model = db.query(models.Stats).filter(models.Stats.user_id == user_id).first()
    # stats_model.amount += receipt.amount

    log_model = models.Log(user_id=user_id,
                           date=datetime.now(),
                           message=f"Added a new receipt with name {receipt_model.name} "
                                   f"and amount {receipt_model.amount}")

    db.add(log_model)
    db.add(receipt_model)
    # db.add(stats_model)
    db.commit()
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
    receipt_model = db.query(models.Receipt).filter(models.Receipt.person_id == person_id).all()
    for receipt in receipt_model:
        db.delete(receipt)
    db.commit()
    stats_model = db.query(models.Stats).filter(models.Stats.user_id == user_id).first()
    stats_model.persons -= 1
    stats_model.amount -= person_model.area
    db.add(stats_model)

    log_model = models.Log(user_id=user_id,
                           date=datetime.now(),
                           message=f"Deleted a person with name {person_model.first_name} {person_model.last_name} "
                                   f"and area {person_model.area} and cnp {person_model.cnp}")

    db.add(log_model)
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


def get_all_receipts_amount(db: Session = Depends(get_db),
                            user_id: int = Depends(auth_handler.auth_wrapper)):
    receipt_model = db.query(models.Receipt).filter(models.Receipt.person_id.in_(
        db.query(models.Person.person_id).filter(models.Person.user_id == user_id))) \
        .filter(extract("year", models.Receipt.date) == datetime.now().year).all()
    if not receipt_model:
        return {"message": "Receipt not found"}
    amount = 0
    for receipt in receipt_model:
        amount += receipt.amount
    return {"amount": round(amount, 2)}


def get_persons_and_amount(db: Session = Depends(get_db),
                           user_id: int = Depends(auth_handler.auth_wrapper)):
    stats = db.query(models.Stats).filter(models.Stats.user_id == user_id).first()
    if not stats:
        return {"persons": 0, "amount": 0}
    return {"persons": stats.persons, "amount": round(stats.amount, 2)}


def edit_person(person_edit: PersonAddDDO, db: Session = Depends(get_db),
                user_id: int = Depends(auth_handler.auth_wrapper)):
    person_to_edit = db.query(models.Person).filter(models.Person.user_id == user_id)\
        .filter(models.Person.person_id == person_edit.person_id).first()

    if person_to_edit:
        person_to_edit.area = person_edit.area
        person_to_edit.quantity = person_edit.quantity
        person_to_edit.cnp  = person_edit.cnp
        person_to_edit.first_name = person_edit.first_name
        person_to_edit.last_name = person_edit.last_name
        db.add(person_to_edit)
        db.commit()
        db.refresh(person_to_edit)
        return {"message": "success"}
    return {"message": "person not found"}
