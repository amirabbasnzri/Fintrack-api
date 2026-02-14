from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserType(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserType), nullable=False, index=True)

    expenses = relationship("ExpenseModel", back_populates="user")

    def __repr__(self):
        return f"<UserModel(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("UserModel", back_populates="expenses", uselist=False)

    def __repr__(self):
        return f"<ExpenseModel(id={self.id}, title='{self.title}', amount={self.amount}, user_id={self.user_id})>"

