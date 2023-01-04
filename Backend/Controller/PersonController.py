from fastapi import Depends, APIRouter
from Service.PersonService import create_person, get_person_by_cnp, get_person_by_name, get_person_by_page

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
