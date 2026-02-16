def test_register_user(client):
    ...


def test_login_user(client, test_user):
    res = client.post("/auth/token", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert res.status_code == 200


def test_get_me(client, access_token, test_user):
    headers = {"Authorization": f"Bearer {access_token}"}
    res = client.get("/auth/me", headers=headers)

    body = res.json()
    assert body["email"] == test_user["email"]
