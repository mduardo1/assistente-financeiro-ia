from src.assistente_financeiro_ia.application.dto.transaction_output import (
    TransactionOutputDTO,
)
from src.assistente_financeiro_ia.domain.repositories.transaction_repository import (
    TransactionRepository,
)


class ListTransactionsUseCase:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self._transaction_repository = transaction_repository

    def execute(self) -> list[TransactionOutputDTO]:
        transactions = self._transaction_repository.list_all()

        return [
            TransactionOutputDTO(
                id=transaction.id,
                description=transaction.description,
                amount=str(transaction.amount),
                transaction_date=transaction.transaction_date.isoformat(),
                category=transaction.category,
            )
            for transaction in transactions
        ]
