from pydantic import BaseModel, EmailStr


class AdminRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    