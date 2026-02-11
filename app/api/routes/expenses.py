from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models import ExpenseModel
from app.db.session import get_session
from app.schemas.expense import ExpenseCreateSchema, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseOut)
def create_expense(
    request: ExpenseCreateSchema,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    expense = ExpenseModel(**request.model_dump(), user_id=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return JSONResponse(
        content={"message": "Expense created successfully"}, status_code=201
    )


@router.get("/", response_model=List[ExpenseOut])
def list_expenses(
    db: Session = Depends(get_session), current_user=Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(ExpenseModel).all()
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id).all()


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    return expense


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    expense_in: ExpenseCreateSchema,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    for field, value in expense_in.model_dump().items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return JSONResponse(
        content={"message": "Expense updated successfully"}, status_code=200
    )


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(expense)
    db.commit()
    return JSONResponse(
        content={"message": "Expense deleted successfully"}, status_code=200
    )
