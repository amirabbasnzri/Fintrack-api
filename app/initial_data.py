from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import UserModel, UserType
from app.core.security import hash_password
from app.core.config import FIRST_ADMIN_NAME, FIRST_ADMIN_EMAIL, FIRST_ADMIN_PASSWORD


def create_first_admin():
    db: Session = SessionLocal()

    admin_exists = db.query(UserModel).filter(UserModel.role == UserType.ADMIN).first()
    if admin_exists:
        db.close()
        return

    email = FIRST_ADMIN_EMAIL
    password = FIRST_ADMIN_PASSWORD
    name = FIRST_ADMIN_NAME

    first_admin = UserModel(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=UserType.ADMIN
    )
    db.add(first_admin)
    db.commit()
    db.refresh(first_admin)
    db.close()
    print("First admin created:", first_admin.email)
