from typing import Protocol

from src.assistente_financeiro_ia.domain.entities.transaction import Transaction


class TransactionRepository(Protocol):
    def list_all(self) -> list[Transaction]:
        """Retorna todas as transacoes cadastradas."""
