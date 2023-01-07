from fastapi import Depends, APIRouter
from Service.PersonService import create_person, get_person_by_cnp, get_person_by_name, get_person_by_page, add_receipt, \
    get_receipt_by_person_id_and_year

person = APIRouter()


@person.post("/add")
def add_person(return_value: dict = Depends(create_person)):
    return return_value


@person.get("/get/{cnp}")
def get_person(return_value: dict = Depends(get_person_by_cnp)):
    return return_value


@person.get("/get")
def get_person(return_value: dict = Depends(get_person_by_name)):
    return return_value


@person.get("/get/{page}/{no_per_page}")
def get_person(return_value: dict = Depends(get_person_by_page)):
    return return_value


@person.post("/add_receipt")
def add_receipt(return_value: dict = Depends(add_receipt)):
    return return_value


@person.get("/get_receipt/{person_id}/{year}")
def get_receipt(return_value: dict = Depends(get_receipt_by_person_id_and_year)):
    return return_value
