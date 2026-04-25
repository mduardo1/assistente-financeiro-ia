from src.assistente_financeiro_ia.domain.entities.transaction import Transaction


class InMemoryTransactionRepository:
    def __init__(self, transactions: list[Transaction] | None = None) -> None:
        self._transactions = transactions or []

    def list_all(self) -> list[Transaction]:
        return list(self._transactions)
