from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    
class UserLoginSchema(BaseModel):
    email: str
    password: str