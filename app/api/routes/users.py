from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.models import UserModel
from app.db.session import get_session
from app.schemas.users import UserRegisterSchema
from app.core.security import hash_password, verify_password

router = APIRouter(tags=["users"])


# registration:
@router.post("/register")
def user_register(request: UserRegisterSchema, db: Session = Depends(get_session)):

    # email validation:
    db_user_email = db.query(UserModel).filter(UserModel.email == request.email).first()
    if db_user_email:
        raise HTTPException(
            detail="Email already registered", status_code=status.HTTP_400_BAD_REQUEST
        )

    # password validation:
    if request.password != request.confirm_password:
        raise HTTPException(
            detail="password and confirm_password do not match",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # hashing password:
    hashed_password = hash_password(request.password)

    # create user:
    user = UserModel(
        name=request.name, email=request.email, hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # successful response:
    return JSONResponse(
        content={
            "Server response": f"User <{user.name}> with email <{user.email}> and id <{user.id}> created successfully"
        },
        status_code=status.HTTP_201_CREATED,
    )

