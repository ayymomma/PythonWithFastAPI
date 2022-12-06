import time

from fastapi import Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from DDO.DocumentDDO import DocumentAddDDO
from DataBase.Database import SessionLocal
import DataBase.Models as models
from Service.UserService import auth_handler


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_document(person_id: int = Form(...),
                 type: str = Form(...),
                 expire_year: int = Form(...),
                 db: Session = Depends(get_db),
                 document: UploadFile = File(...),
                 user_id: int = Depends(auth_handler.auth_wrapper)):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    document_name = f"{type}_{timestr}_{document.filename.replace(' ', '_')}"
    with open(f"Documents/{document_name}", "wb+") as buffer:
        content = document.file.read()
        buffer.write(content)
    document_model = models.Document(person_id=person_id,
                                     document_code=document_name,
                                     type=type,
                                     expire_year=expire_year)
    db.add(document_model)
    db.commit()
    db.refresh(document_model)
    return {"message": "Document added"}
