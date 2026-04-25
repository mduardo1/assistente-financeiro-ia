from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    id: int
    user_id: int
    type: str
    description: str
    category: str
    amount: float
    source: str
    transaction_date: str
    created_at: str
