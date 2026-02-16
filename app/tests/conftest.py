import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from app.core.security import create_access_token, hash_password
from app.main import app
from app.db.base import Base
from app.db.session import get_session
from app.db.models import ExpenseModel, UserModel, UserType

fake = Faker()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as c:
        yield c



@pytest.fixture
def create_test_users(db_session):
    fake.unique.clear()

    admin = UserModel(
        name="admin",
        email="admin@example.com",
        hashed_password=hash_password("Admin12@"),
        role="admin",
    )
    db_session.add(admin)

    users = []
    for _ in range(5):
        u = UserModel(
            name=fake.user_name(),
            email=fake.unique.email(),
            hashed_password=hash_password("Password12@"),
        )
        db_session.add(u)
        users.append(u)

    db_session.commit()

    for u in users:
        for _ in range(3):
            db_session.add(
                ExpenseModel(
                    title=fake.word(),
                    amount=100,
                    description=fake.sentence(),
                    user_id=u.id,
                )
            )

    db_session.commit()
    return users


@pytest.fixture
def test_user(client):
    data = {
        "name": "John",
        "email": "john@test.com",
        "password": "Test1234!",
        "confirm_password": "Test1234!"
    }
    client.post("/auth/register", json=data)
    return data


@pytest.fixture
def access_token(client, test_user):
    res = client.post("/auth/token", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    return res.json()["access_token"]


@pytest.fixture
def admin_user(db_session):
    admin = UserModel(
        name="SuperAdmin",
        email="admin@test.com",
        hashed_password=hash_password("Admin123!"),
        role=UserType.ADMIN,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def admin_token(admin_user):
    return create_access_token(
        {"sub": str(admin_user.id), "role": admin_user.role}
    )

@pytest.fixture
def admin_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }

@pytest.fixture
def normal_user(db_session):
    user = UserModel(
        name="John",
        email="john@test.com",
        hashed_password=hash_password("Test1234!"),
        role=UserType.USER,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def user_token(normal_user):
    return create_access_token(
        {"sub": str(normal_user.id), "role": normal_user.role}
    )

@pytest.fixture
def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}
