from datetime import datetime
from decimal import Decimal, InvalidOperation

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
        amount_raw = form_data.get("amount", "").strip()
        transaction_date = form_data.get("transaction_date", "").strip()

        if transaction_type not in self.VALID_TYPES:
            return False, "Selecione um tipo de movimentação válido."

        if not description:
            return False, "A descrição é obrigatória."

        if not category:
            return False, "A categoria é obrigatória."

        if not amount_raw:
            return False, "O valor é obrigatório."

        if not transaction_date:
            return False, "A data é obrigatória."

        try:
            amount = self.parse_amount(amount_raw)
        except ValueError as error:
            return False, str(error)

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
                float(amount),
                source,
                transaction_date,
            ),
        )
        connection.commit()
        return True, "Movimentação registrada com sucesso."

    def list_transactions(
        self,
        user_id: int,
        filters: dict[str, str] | None = None,
    ) -> list[Transaction]:
        filters = filters or {}
        query = """
            SELECT id, user_id, type, description, category, amount, source,
                   transaction_date, created_at
            FROM transactions
            WHERE user_id = ?
        """
        params: list[object] = [user_id]

        transaction_type = filters.get("type", "").strip()
        category = filters.get("category", "").strip().lower()
        date_start = filters.get("date_start", "").strip()
        date_end = filters.get("date_end", "").strip()

        if transaction_type in self.VALID_TYPES:
            query += " AND type = ?"
            params.append(transaction_type)

        if category:
            query += " AND category = ?"
            params.append(category)

        if date_start:
            query += " AND transaction_date >= ?"
            params.append(date_start)

        if date_end:
            query += " AND transaction_date <= ?"
            params.append(date_end)

        query += " ORDER BY transaction_date DESC, id DESC"

        connection = get_db()
        rows = connection.execute(query, tuple(params)).fetchall()

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

    def list_categories(self, user_id: int) -> list[str]:
        connection = get_db()
        rows = connection.execute(
            """
            SELECT DISTINCT category
            FROM transactions
            WHERE user_id = ?
            ORDER BY category ASC
            """,
            (user_id,),
        ).fetchall()

        return [str(row["category"]) for row in rows]

    def parse_amount(self, amount_raw: str) -> Decimal:
        normalized = amount_raw.strip().replace(",", ".")

        if not normalized:
            raise ValueError("O valor é obrigatório.")

        try:
            amount = Decimal(normalized)
        except InvalidOperation as error:
            raise ValueError("Informe um valor numérico válido.") from error

        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        return amount.quantize(Decimal("0.01"))
