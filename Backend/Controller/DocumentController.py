from fastapi import APIRouter, Depends

from Service.DocumentService import add_document

document = APIRouter()


@document.post("/add", status_code=201)
def add_document(return_value: dict = Depends(add_document)):
    return return_value
