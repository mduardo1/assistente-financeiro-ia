from dataclasses import dataclass
from datetime import date

from src.assistente_financeiro_ia.domain.value_objects.money import Money


@dataclass(frozen=True)
class Transaction:
    id: str
    description: str
    amount: Money
    transaction_date: date
    category: str
