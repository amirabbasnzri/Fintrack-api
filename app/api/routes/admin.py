from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.security import create_access_token, hash_password
from app.db.models import UserModel, UserType
from app.db.session import get_session
from app.schemas.admin import AdminRegisterSchema

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.post("/register")
def register_admin(
    admin_in: AdminRegisterSchema,
    db: Session = Depends(get_session),
    admin=Depends(get_current_admin),
):
    if db.query(UserModel).filter(UserModel.email == admin_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
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
def list_users(db: Session = Depends(get_session), admin=Depends(get_current_admin)):
    return db.query(UserModel).all()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int, db: Session = Depends(get_session), admin=Depends(get_current_admin)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}
