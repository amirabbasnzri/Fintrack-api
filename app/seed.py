import os
import random

from faker import Faker
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import ExpenseModel, UserModel
from app.db.session import SessionLocal

fake = Faker()


def seed_data():
    db: Session = SessionLocal()
    admin_exists = db.query(UserModel).filter(UserModel.role == "admin").first()
    if admin_exists:
        db.close()
        return False

    first_admin_email = os.getenv("FIRST_ADMIN_EMAIL")
    first_admin_password = os.getenv("FIRST_ADMIN_PASSWORD")
    first_admin_username = os.getenv("FIRST_ADMIN_USERNAME")

    first_admin = UserModel(
        name=first_admin_username,
        email=first_admin_email,
        hashed_password=hash_password(first_admin_password),
        role="admin",
    )
    db.add(first_admin)

    users = []
    for _ in range(15):
        user = UserModel(
            name=fake.user_name(),
            email=fake.unique.email(),
            hashed_password=hash_password("Password123"),
            role="user",
        )
        db.add(user)
        users.append(user)
    db.commit()
    for u in users:
        db.refresh(u)

    for user in users:
        for _ in range(10):
            expense = ExpenseModel(
                title=fake.word().capitalize(),
                amount=round(random.uniform(10, 500), 2),
                description=fake.sentence(),
                user_id=user.id,
            )
            db.add(expense)
    db.commit()
    db.close()
    return True
