from dataclasses import dataclass


@dataclass(frozen=True)
class TransactionOutputDTO:
    id: str
    description: str
    amount: str
    transaction_date: str
    category: str
