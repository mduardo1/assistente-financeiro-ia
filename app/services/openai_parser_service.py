import json
from typing import Any

from flask import current_app

from app.services.parser_service import ParserService


class OpenAIParserService:
    """
    Usa OpenAI Structured Outputs quando configurado.
    Caso a API não esteja disponível, faz fallback para o parser local.
    """

    def __init__(self) -> None:
        self._local_parser = ParserService()

    def parse_message(self, message: str) -> dict[str, str]:
        if not current_app.config.get("USE_OPENAI_PARSER") or not current_app.config.get("OPENAI_API_KEY"):
            return self._local_parser.parse_message(message)

        try:
            payload = self._parse_with_openai(message)
            return self._local_parser.validate_parsed_payload(payload)
        except Exception:
            return self._local_parser.parse_message(message)

    def _parse_with_openai(self, message: str) -> dict[str, Any]:
        try:
            from openai import OpenAI
        except ImportError as error:
            raise RuntimeError("Biblioteca OpenAI não está instalada.") from error

        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "Você extrai movimentações financeiras em JSON. "
                        "Retorne type (income|expense), amount, category, description e transaction_date."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Interprete a mensagem financeira a seguir e devolva JSON válido. "
                        f"Mensagem: {message}"
                    ),
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "financial_transaction",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["income", "expense"]},
                            "amount": {"type": "number"},
                            "category": {"type": "string"},
                            "description": {"type": "string"},
                            "transaction_date": {"type": "string"},
                        },
                        "required": [
                            "type",
                            "amount",
                            "category",
                            "description",
                            "transaction_date",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
        )

        output_text = getattr(response, "output_text", "")
        if not output_text:
            raise ValueError("A IA não conseguiu interpretar a mensagem.")

        payload = json.loads(output_text)
        if not isinstance(payload, dict):
            raise ValueError("A IA retornou um JSON inválido.")

        return payload
