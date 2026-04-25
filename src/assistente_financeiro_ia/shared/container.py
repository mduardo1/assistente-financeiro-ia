from dataclasses import dataclass

from src.assistente_financeiro_ia.application.use_cases.health_check import HealthCheckUseCase
from src.assistente_financeiro_ia.application.use_cases.list_transactions import ListTransactionsUseCase
from src.assistente_financeiro_ia.infrastructure.repositories.in_memory_transaction_repository import (
    InMemoryTransactionRepository,
)
from src.assistente_financeiro_ia.shared.config.settings import Settings


@dataclass(frozen=True)
class Container:
    settings: Settings
    health_check_use_case: HealthCheckUseCase
    list_transactions_use_case: ListTransactionsUseCase

    @classmethod
    def build(cls, settings: Settings) -> "Container":
        transaction_repository = InMemoryTransactionRepository()

        return cls(
            settings=settings,
            health_check_use_case=HealthCheckUseCase(settings=settings),
            list_transactions_use_case=ListTransactionsUseCase(
                transaction_repository=transaction_repository
            ),
        )
