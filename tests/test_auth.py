from app.database.connection import get_db


def test_register_creates_user(client, app):
    response = client.post(
        "/auth/register",
        data={
            "name": "Moyses",
            "email": "moyses@example.com",
            "password": "123456",
            "whatsapp": "11999999999",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Conta criada com sucesso" in response.data

    with app.app_context():
        row = get_db().execute(
            "SELECT email, password_hash FROM users WHERE email = ?",
            ("moyses@example.com",),
        ).fetchone()

    assert row is not None
    assert row["email"] == "moyses@example.com"
    assert row["password_hash"] != "123456"


def test_login_creates_session(client):
    client.post(
        "/auth/register",
        data={
            "name": "Moyses",
            "email": "moyses@example.com",
            "password": "123456",
            "whatsapp": "",
        },
    )

    response = client.post(
        "/auth/login",
        data={"email": "moyses@example.com", "password": "123456"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Login realizado com sucesso" in response.data
    assert "Movimentações registradas".encode("utf-8") in response.data
