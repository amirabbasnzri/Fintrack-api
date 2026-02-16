def test_create_expense(client, user_headers):
    data = {
        "title": "Lunch",
        "amount": 12.5,
        "description": "Burger"
    }

    client.cookies.set("lang", "en")
    res = client.post("/expenses/", json=data, headers=user_headers)

    assert res.status_code == 201
    body = res.json()
    assert body["expense"]["title"] == "Lunch"


def test_list_expenses(client, user_headers):
    res = client.get("/expenses/", headers=user_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_expense(client, db_session, normal_user, user_headers):
    from app.db.models import ExpenseModel

    expense = ExpenseModel(
        title="Coffee",
        amount=5,
        description="Latte",
        user_id=normal_user.id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    res = client.get(f"/expenses/{expense.id}", headers=user_headers)
    assert res.status_code == 200
    assert res.json()["expense"]["title"] == "Coffee"

def test_update_expense(client, db_session, normal_user, user_headers):
    from app.db.models import ExpenseModel

    expense = ExpenseModel(
        title="Old",
        amount=10,
        description="Old desc",
        user_id=normal_user.id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    data = {"title": "New", "amount": 99, "description": "Updated"}

    res = client.put(f"/expenses/{expense.id}", json=data, headers=user_headers)
    assert res.status_code == 200

def test_delete_expense(client, db_session, normal_user, user_headers):
    from app.db.models import ExpenseModel

    expense = ExpenseModel(
        title="Temp",
        amount=1,
        description="tmp",
        user_id=normal_user.id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    res = client.delete(f"/expenses/{expense.id}", headers=user_headers)
    assert res.status_code == 200

def test_get_expense_forbidden(client, db_session, normal_user, user_headers):
    from app.db.models import UserModel, ExpenseModel
    from app.core.security import hash_password

    other = UserModel(
        name="Other",
        email="other@test.com",
        hashed_password=hash_password("1234"),
        role="user",
    )
    db_session.add(other)
    db_session.commit()
    db_session.refresh(other)

    expense = ExpenseModel(
        title="Secret",
        amount=999,
        description="hack",
        user_id=other.id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    res = client.get(f"/expenses/{expense.id}", headers=user_headers)
    assert res.status_code == 403

