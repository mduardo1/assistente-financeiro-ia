import pytest

from app.services.openai_parser_service import OpenAIParserService
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


def test_validate_parsed_payload_rejects_negative_amount():
    with pytest.raises(ValueError, match="valor negativo"):
        ParserService().validate_parsed_payload(
            {
                "type": "expense",
                "amount": -50,
                "category": "mercado",
                "description": "gastei 50 no mercado",
                "transaction_date": "2026-04-25",
            }
        )


def test_validate_parsed_payload_defaults_missing_date():
    parsed = ParserService().validate_parsed_payload(
        {
            "type": "expense",
            "amount": 50,
            "category": "mercado",
            "description": "gastei 50 no mercado",
            "transaction_date": None,
        }
    )

    assert parsed["transaction_date"]


def test_openai_parser_service_uses_local_fallback(app):
    with app.app_context():
        parsed = OpenAIParserService().parse_message("paguei 120 de internet")

    assert parsed["type"] == "expense"
    assert parsed["category"] == "internet"


def test_openai_parser_service_falls_back_on_invalid_ai_payload(app, monkeypatch):
    def fake_parse(_message: str):
        return {"type": "income", "amount": -10}

    with app.app_context():
        monkeypatch.setattr(OpenAIParserService, "_parse_with_openai", lambda self, message: fake_parse(message))
        app.config["USE_OPENAI_PARSER"] = True
        app.config["OPENAI_API_KEY"] = "test-key"
        parsed = OpenAIParserService().parse_message("recebi 300 de cliente")

    assert parsed["type"] == "income"
    assert parsed["category"] == "cliente"
