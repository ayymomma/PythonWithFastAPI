from pydantic import BaseModel, Field


class PersonDDO(BaseModel):
    person_id: int
    first_name: str
    last_name: str
    phone: str


class PersonSearchDDO(BaseModel):
    first_name: str
    last_name: str


class PersonSearchCNPDDO(BaseModel):
    cnp: str
