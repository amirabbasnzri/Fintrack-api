def test_set_language_cookie(client):
    data = {"lang": "fa"}

    res = client.post("/i18n/set-language/fa", json=data)

    assert res.status_code == 200
    assert res.cookies.get("lang") == "fa"

def test_set_language_response(client):
    data = {"lang": "en"}
    res = client.post("/i18n/set-language/en", json=data)

    body = res.json()
    assert "message" in body

