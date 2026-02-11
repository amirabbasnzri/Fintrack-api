from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from app.db.base import Base
from enum import Enum



class UserType(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserType), nullable=False)
    
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"
    
    
