from pydantic import BaseModel, Field


class PersonAddDDO(BaseModel):
    person_id: int
    first_name: str
    last_name: str
    phone: str
    area: float
    quantity: int
    cnp: str


class PersonSearchDDO(BaseModel):
    first_name: str
    last_name: str
    user_id: int


class PersonSearchCNPDDO(BaseModel):
    cnp: str
    user_id: int
