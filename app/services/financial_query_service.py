from app.database.connection import get_db


class FinancialQueryService:
    """Base inicial para futuras consultas financeiras por texto."""

    def can_handle(self, message: str) -> bool:
        normalized_message = message.strip().lower()
        supported_questions = (
            "quanto gastei hoje",
            "quanto tenho em caixa",
            "qual categoria mais gastei",
        )
        return any(question in normalized_message for question in supported_questions)

    def summarize_capabilities(self) -> dict[str, list[str]]:
        return {
            "supported_examples": [
                "quanto gastei hoje?",
                "quanto tenho em caixa?",
                "qual categoria mais gastei?",
            ],
            "status": ["planned"],
        }

    def get_current_balance(self, user_id: int) -> float:
        connection = get_db()
        row = connection.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) -
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) AS balance
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        return float(row["balance"])
