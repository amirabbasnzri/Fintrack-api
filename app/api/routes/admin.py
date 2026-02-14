from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.security import create_access_token, hash_password
from app.db.models import ExpenseModel, UserModel, UserType
from app.db.session import get_session
from app.schemas.admin import AdminRegisterSchema
from app.i18n.middleware import t

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.post("/register")
def register_admin(
    request: Request,
    admin_in: AdminRegisterSchema,
    db: Session = Depends(get_session),
    admin=Depends(get_current_admin),
):
    
    # set language:
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    if db.query(UserModel).filter(UserModel.email == admin_in.email).first():
        raise HTTPException(status_code=400, detail=t("EMAIL_EXISTS", lang))
    new_admin = UserModel(
        name=admin_in.name,
        email=admin_in.email,
        hashed_password=hash_password(admin_in.password),
        role=UserType.ADMIN,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    access_token = create_access_token(
        data={"sub": str(new_admin.id), "role": new_admin.role}
    )
    response = {
        'msg': t("ADMIN_CREATED_SUCCESS", lang),
        "id": new_admin.id,
        "name": new_admin.name,
        "email": new_admin.email,
        "role": new_admin.role,
        "access_token": access_token,
        "token_type": "bearer",
    }

    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/users")
def list_users(request: Request, db: Session = Depends(get_session), admin=Depends(get_current_admin)):
    lang = request.cookies.get("lang", "en") if request else 'en'
    users = db.query(UserModel).all()
    response = {
        'msg': t("USERS_LIST_RETRIEVED", lang),
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
            for user in users
        ]
    }
    return response

@router.delete("/users/{user_id}")
def delete_user(
    request: Request,
    user_id: int, db: Session = Depends(get_session), admin=Depends(get_current_admin)
):
    # set language:
    lang = request.cookies.get("lang", "en") if request else 'en'
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    user_expense = db.query(ExpenseModel).filter(ExpenseModel.user_id == user_id).all()
    if not user:
        raise HTTPException(status_code=404, detail=t("USER_NOT_FOUND", lang))
    for e in user_expense:
        db.delete(e)
    db.delete(user)
    db.commit()
    return JSONResponse(content={'msg': t("USER_DELETED", lang)})
