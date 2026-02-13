from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    def strong_password(self) -> bool:
        has_upper = any(char.isupper() for char in self.password)
        has_lower = any(char.islower() for char in self.password)
        has_digit = any(char.isdigit() for char in self.password)
        has_special = any(not char.isalnum() for char in self.password)
        return all([has_upper, has_lower, has_digit, has_special])


class UserLoginSchema(BaseModel):
    email: str
    password: str
