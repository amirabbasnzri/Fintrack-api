from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.models import UserModel
from app.db.session import get_session
from app.schemas.users import UserRegisterSchema, UserLoginSchema
from app.core.security import hash_password, is_password_confirmed, verify_password, create_access_token, verify_email_not_exists
from app.api.deps import get_current_user



router = APIRouter(prefix="/auth", tags=["auth"])


# registration:
@router.post("/register")
def user_register(request: UserRegisterSchema, db: Session = Depends(get_session)):

    # email validation:
    verify_email_not_exists(db, request.email)

    # password confirmation validation:
    is_password_confirmed(request.password, request.confirm_password)
    
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
    access_token = create_access_token(data={"sub": str(user.id)})
    response = {
        "msg": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
    )




@router.post("/token")
def login(request: UserLoginSchema, db: Session = Depends(get_session)):
    # validation:
    db_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if db_user is not None:
        is_verified = verify_password(request.password, db_user.hashed_password)
 
    if not db_user or not is_verified:
        raise HTTPException(
            detail="Email not found or incorrect password", status_code=status.HTTP_400_BAD_REQUEST
        )
        
    access_token = create_access_token(data={"sub": str(db_user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/me")
def read_current_user(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }

