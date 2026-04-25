from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str
    password_hash: str
    whatsapp: str | None
    created_at: str
