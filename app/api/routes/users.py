from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (
    create_access_token,
    hash_password,
    is_password_confirmed,
    verify_email_not_exists,
    verify_email_and_password,
)
from app.db.models import UserModel, UserType
from app.db.session import get_session
from app.schemas.users import UserLoginSchema, UserRegisterSchema
from app.i18n.middleware import t

router = APIRouter(prefix="/auth", tags=["auth"])


# registration:
@router.post("/register")
def user_register(user: UserRegisterSchema, db: Session = Depends(get_session), request: Request = None):
    
    # set language
    lang = request.cookies.get("lang", "en")
    
    
    # email validation:
    verify_email_not_exists(db, user.email, lang)

    # password confirmation validation:
    is_password_confirmed(user.password, user.confirm_password, lang)

    # strong password:
    if not user.strong_password():
        raise HTTPException(
            detail="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (like: !@#$%^&*)",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # hashing password:
    hashed_password = hash_password(user.password)

    # create user:
    new_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=UserType.USER,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # successful response:
    access_token = create_access_token(data={"sub": str(new_user.id)})
    response = {
        "msg": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer",
    }

    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/token")
def login(user: UserLoginSchema, db: Session = Depends(get_session), request: Request = None):
    # set language
    lang = request.cookies.get("lang", "en")
    
    # validation:
    db_user = verify_email_and_password(db, user, lang)
    # create access token:
    access_token = create_access_token(data={"sub": str(db_user.id)})

    # message:
    msg = f'{t("HELLO_USER", lang, name= db_user.name)}, {t("LOGIN_SUCCESS", lang)}'
    response = {
        "message": msg,
        "access_token": access_token,
        "token_type": "bearer",
    }

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@router.get("/me")
def read_current_user(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
    }
