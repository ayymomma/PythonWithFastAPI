from datetime import datetime
from pydantic import BaseModel


class ReceiptAddDDO(BaseModel):
    name: str
    date: datetime
    amount: int
    person_id: int

