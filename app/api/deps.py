from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY, ALGORITHM
from app.db.session import get_session
from app.db.models import UserModel, UserType
from app.core.security import credentials_exception


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_session)) -> UserModel:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception()
    except JWTError:
        raise credentials_exception()
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception()
    return user


def get_current_admin(user: UserModel = Depends(get_current_user)):
    if user.role == UserType.ADMIN:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden access to endpoint",
    )