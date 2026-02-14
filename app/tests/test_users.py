import uuid

def test_register_user(client):
    data = {
        "name": "John",
        "email": f"{uuid.uuid4()}@test.com",
        "password": "VeryStrongPass123!!!",
        "confirm_password": "VeryStrongPass123!!!"

    }

    client.cookies.set("lang", "en")
    res = client.post("/auth/register", json=data)

    assert res.status_code == 201
    assert res.status_code == 201
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_user(client):
    data = {
        "email": "john@test.com",
        "password": "Test1234!"
    }

    client.cookies.set("lang", "en")
    res = client.post("/auth/token", json=data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert "message" in body

    global ACCESS_TOKEN
    ACCESS_TOKEN = body["access_token"]


def test_get_me(client):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    client.cookies.set("lang", "en")
    res = client.get("/auth/me", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["email"] == "john@test.com"
    assert body["name"] == "John"
