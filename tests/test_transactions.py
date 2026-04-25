import pytest

from app.services.transaction_service import TransactionService


def login_default_user(client):
    client.post(
        "/auth/register",
        data={
            "name": "Moyses",
            "email": "moyses@example.com",
            "password": "123456",
            "whatsapp": "",
        },
    )
    client.post(
        "/auth/login",
        data={"email": "moyses@example.com", "password": "123456"},
    )


def test_create_transaction_redirects_after_success(client):
    login_default_user(client)

    response = client.post(
        "/transactions/",
        data={
            "type": "income",
            "description": "Venda de movel",
            "category": "moveis",
            "amount": "500",
            "transaction_date": "2026-04-25",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")


def test_create_transaction_accepts_comma_value(client):
    login_default_user(client)

    client.post(
        "/transactions/",
        data={
            "type": "expense",
            "description": "Compra no mercado",
            "category": "mercado",
            "amount": "50,25",
            "transaction_date": "2026-04-25",
        },
    )

    response = client.get("/transactions/")

    assert response.status_code == 200
    assert "R$ 50.25".encode("utf-8") in response.data


def test_create_transaction_accepts_dot_value(client):
    login_default_user(client)

    client.post(
        "/transactions/",
        data={
            "type": "expense",
            "description": "Internet",
            "category": "internet",
            "amount": "120.90",
            "transaction_date": "2026-04-25",
        },
    )

    response = client.get("/transactions/")

    assert response.status_code == 200
    assert "R$ 120.90".encode("utf-8") in response.data


def test_create_transaction_rejects_negative_value(client):
    login_default_user(client)

    response = client.post(
        "/transactions/",
        data={
            "type": "expense",
            "description": "Compra inválida",
            "category": "teste",
            "amount": "-50",
            "transaction_date": "2026-04-25",
        },
    )

    assert response.status_code == 400
    assert "O valor deve ser maior que zero.".encode("utf-8") in response.data


def test_parse_amount_rejects_invalid_value():
    service = TransactionService()

    with pytest.raises(ValueError, match="Informe um valor numérico válido."):
        service.parse_amount("abc")


def test_transaction_filters_by_type_and_category(client):
    login_default_user(client)
    client.post(
        "/transactions/",
        data={
            "type": "income",
            "description": "Venda",
            "category": "cliente",
            "amount": "300",
            "transaction_date": "2026-04-25",
        },
    )
    client.post(
        "/transactions/",
        data={
            "type": "expense",
            "description": "Mercado",
            "category": "mercado",
            "amount": "50",
            "transaction_date": "2026-04-25",
        },
    )

    response = client.get("/transactions/?type=expense&category=mercado")

    assert response.status_code == 200
    assert b"Mercado" in response.data
    assert b"Venda" not in response.data
