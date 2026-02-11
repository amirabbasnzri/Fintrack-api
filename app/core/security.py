from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.db.models import UserModel



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def is_password_confirmed(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(
            detail="password and confirm_password do not match",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def verify_email_not_exists(db, email: str):
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        raise HTTPException(
            detail="Email already registered", status_code=status.HTTP_400_BAD_REQUEST
        )
        


