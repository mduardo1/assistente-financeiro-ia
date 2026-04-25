from dataclasses import dataclass

from app.services.openai_parser_service import OpenAIParserService
from app.services.transaction_service import TransactionService


@dataclass(frozen=True)
class SavedMessageTransaction:
    parsed_data: dict[str, str]
    success_message: str


class MessageTransactionService:
    def __init__(self) -> None:
        self._parser_service = OpenAIParserService()
        self._transaction_service = TransactionService()

    def parse_and_save(
        self,
        user_id: int,
        message: str,
        source: str,
    ) -> SavedMessageTransaction:
        parsed_data = self._parser_service.parse_message(message)
        success, service_message = self._transaction_service.create_transaction(
            user_id=user_id,
            form_data=parsed_data,
            source=source,
        )

        if not success:
            raise ValueError(service_message)

        return SavedMessageTransaction(
            parsed_data=parsed_data,
            success_message=service_message,
        )
