import uuid


def test_register_admin(client, admin_headers):
    data = {
        "name": "New Admin",
        "email": f"{uuid.uuid4()}@admin.com",
        "password": "Admin123!",
        "confirm_password": "Admin123!",
    }

    client.cookies.set("lang", "en")
    res = client.post("/admin/register", json=data, headers=admin_headers)

    assert res.status_code == 201
    body = res.json()
    assert "access_token" in body
    assert body["role"] == "admin"

def test_list_users(client, admin_headers):
    client.cookies.set("lang", "en")
    res = client.get("/admin/users", headers=admin_headers)

    assert res.status_code == 200
    body = res.json()
    assert "users" in body
    assert isinstance(body["users"], list)

def test_delete_user(client, db_session, admin_headers):
    # create user manually
    from app.db.models import UserModel
    from app.core.security import hash_password

    user = UserModel(
        name="TestUser",
        email="user@test.com",
        hashed_password=hash_password("Test1234!"),
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    client.cookies.set("lang", "en")
    res = client.delete(f"/admin/users/{user.id}", headers=admin_headers)

    assert res.status_code == 200
    body = res.json()
    assert "USER_DELETED" in body["msg"] or "deleted" in body["msg"].lower()
