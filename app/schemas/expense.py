from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExpenseBase(BaseModel):
    title: str
    amount: float
    description: str | None = None


class ExpenseCreateSchema(ExpenseBase):
    pass

