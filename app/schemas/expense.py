from pydantic import BaseModel
from datetime import datetime

class ExpenseBase(BaseModel):
    title: str
    amount: float
    description: str | None = None

class ExpenseCreateSchema(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime
