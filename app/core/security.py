from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
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


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )