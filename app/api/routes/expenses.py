from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models import ExpenseModel
from app.db.session import get_session
from app.schemas.expense import ExpenseCreateSchema
from app.i18n.middleware import t

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/")
def create_expense(
    request: Request,
    expense: ExpenseCreateSchema,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # set language:
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    # create expense:
    expense = ExpenseModel(**expense.model_dump(), user_id=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    
    # json response:
    response = {
        'title': expense.title,
        'amount': expense.amount,
        'description': expense.description,
        'created_at': expense.created_at.isoformat(),
        'user_id': expense.user_id,
    }
    
    # successful response:
    return JSONResponse(
        content={
            "msg": t("EXPENSE_CREATED", lang),
            "expense": response
                 },
        status_code=201
        )


@router.get("/")
def list_expenses(
    request: Request,
    db: Session = Depends(get_session), current_user=Depends(get_current_user)
):
    # set language:
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    if current_user.role == "admin":
        return db.query(ExpenseModel).all()
    
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id).all()


@router.get("/{expense_id}")
def get_expense(
    request: Request,
    expense_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # set language:
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail=t("EXPENSE_NOT_FOUND", lang))
    if expense.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("NOT_ALLOWED", lang))
    
    # json response:
    response = {
        "title": expense.title,
        "amount": expense.amount,
        "description": expense.description,
        "created_at": expense.created_at.isoformat(),
        "user_id": expense.user_id,
    }
    # successful response:
    return JSONResponse(
        content={
            "msg": t("EXPENSE_FETCHED", lang),
            "expense": response
            },
        status_code=200)

# edit expense:
@router.put("/{expense_id}")
def update_expense(
    request: Request,
    expense_id: int,
    expense_in: ExpenseCreateSchema,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # set language: 
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail=t("EXPENSE_NOT_FOUND", lang))
    if expense.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("NOT_ALLOWED", lang))

    for field, value in expense_in.model_dump().items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return JSONResponse(
        content={"message": t("EXPENSE_UPDATED", lang)}, status_code=200
    )


@router.delete("/{expense_id}")
def delete_expense(
    request: Request,
    expense_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # set language: 
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail=t("EXPENSE_NOT_FOUND", lang))
    if expense.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("NOT_ALLOWED", lang))
    db.delete(expense)
    db.commit()
    return JSONResponse(
        content={"message": t("EXPENSE_DELETED", lang)}, status_code=200
    )
    

