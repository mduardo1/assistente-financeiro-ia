import pytest

from app.services.parser_service import ParserService


def test_parser_understands_expense_message():
    parsed = ParserService().parse_message("gastei 50 no mercado")

    assert parsed["type"] == "expense"
    assert parsed["amount"] == "50"
    assert parsed["category"] == "mercado"


def test_parser_understands_income_message():
    parsed = ParserService().parse_message("vendi 500 em moveis")

    assert parsed["type"] == "income"
    assert parsed["amount"] == "500"
    assert parsed["category"] == "moveis"


def test_parser_understands_complex_income_message():
    parsed = ParserService().parse_message("ganhei 1000 da venda do iphone")

    assert parsed["type"] == "income"
    assert parsed["amount"] == "1000"
    assert parsed["category"] == "venda do iphone"


def test_parser_rejects_empty_message():
    with pytest.raises(ValueError, match="A mensagem do parser é obrigatória."):
        ParserService().parse_message("")


def test_parser_route_creates_transaction_from_message(client):
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

    response = client.post(
        "/transactions/parse",
        data={"message": "paguei 120 de internet"},
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
