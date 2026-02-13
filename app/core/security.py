from datetime import datetime, timedelta

from fastapi import HTTPException, status, Request
from jose import jwt
from passlib.context import CryptContext

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.db.models import UserModel
from app.i18n.middleware import t


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_email_and_password(db, user, lang):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user is not None:
        is_verified = pwd_context.verify(user.password, db_user.hashed_password)

    if not db_user or not is_verified:
        raise HTTPException(
            detail=t("INVALID_CREDENTIALS", lang),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return db_user


def is_password_confirmed(password: str, confirm_password: str, lang):
    if password != confirm_password:
        raise HTTPException(
            detail=t("PASSWORDS_NOT_MATCH", lang=lang),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def verify_email_not_exists(db, email: str, lang):
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        raise HTTPException(
            detail= t("EMAIL_EXISTS", lang=lang),
            status_code=status.HTTP_400_BAD_REQUEST
        )


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
