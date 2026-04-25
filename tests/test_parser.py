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

    assert response.status_code == 200
    assert "Mensagem interpretada e movimentação salva com sucesso.".encode("utf-8") in response.data
    assert "internet".encode("utf-8") in response.data
