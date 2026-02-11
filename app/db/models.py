from sqlalchemy import Column, Integer, String
from app.db.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        return f"<UserModel(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    
