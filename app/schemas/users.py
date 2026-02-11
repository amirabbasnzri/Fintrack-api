from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str