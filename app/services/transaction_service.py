from datetime import datetime

from app.database.connection import get_db
from app.models.transaction import Transaction


class TransactionService:
    VALID_TYPES = {"income", "expense"}

    def create_transaction(
        self,
        user_id: int,
        form_data: dict[str, str],
        source: str = "manual",
    ) -> tuple[bool, str]:
        transaction_type = form_data.get("type", "").strip()
        description = form_data.get("description", "").strip()
        category = form_data.get("category", "").strip().lower()
        amount_raw = form_data.get("amount", "").strip().replace(",", ".")
        transaction_date = form_data.get("transaction_date", "").strip()

        if transaction_type not in self.VALID_TYPES:
            return False, "Selecione um tipo de movimentação válido."

        if not description or not category or not amount_raw or not transaction_date:
            return False, "Preencha descrição, categoria, valor e data."

        try:
            amount = float(amount_raw)
        except ValueError:
            return False, "Informe um valor numérico válido."

        if amount <= 0:
            return False, "O valor deve ser maior que zero."

        try:
            datetime.strptime(transaction_date, "%Y-%m-%d")
        except ValueError:
            return False, "Informe uma data válida no formato AAAA-MM-DD."

        connection = get_db()
        connection.execute(
            """
            INSERT INTO transactions (
                user_id, type, description, category, amount, source, transaction_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                transaction_type,
                description,
                category,
                amount,
                source,
                transaction_date,
            ),
        )
        connection.commit()
        return True, "Movimentação registrada com sucesso."

    def list_transactions(self, user_id: int) -> list[Transaction]:
        connection = get_db()
        rows = connection.execute(
            """
            SELECT id, user_id, type, description, category, amount, source,
                   transaction_date, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY transaction_date DESC, id DESC
            """,
            (user_id,),
        ).fetchall()

        return [
            Transaction(
                id=row["id"],
                user_id=row["user_id"],
                type=row["type"],
                description=row["description"],
                category=row["category"],
                amount=row["amount"],
                source=row["source"],
                transaction_date=row["transaction_date"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
