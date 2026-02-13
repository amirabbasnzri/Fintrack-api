from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import ALGORITHM, SECRET_KEY
from app.db.models import UserModel, UserType
from app.db.session import get_session
from app.i18n.middleware import t


security = HTTPBearer()


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session),
    
) -> UserModel:
    # set language:
    lang = request.cookies.get('lang', 'en') if request else "en"
    
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= t("INVALID_TOKEN", lang),
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= t("INVALID_TOKEN", lang),
        )
        
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= t("USER_NOT_FOUND", lang),
    )
    return user


def get_current_admin(user: UserModel = Depends(get_current_user), request: Request = None):
    # set language:
    lang = request.cookies.get('lang', 'en') if request else 'en'
    if user.role == UserType.ADMIN:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail= t("FORBIDDEN_ACCESS", lang),
    )
