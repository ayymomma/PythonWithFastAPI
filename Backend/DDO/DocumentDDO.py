from pydantic import BaseModel


class DocumentAddDDO(BaseModel):
    person_id: int
    type: str | None = None
    expire_year: int


class DocumentSearchDDO(BaseModel):
    person_id: int
    type: str | None = None

