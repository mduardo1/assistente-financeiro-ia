from datetime import date

from app.database.connection import get_db


class FinancialQueryService:
    """Consultas financeiras locais simples para o dashboard."""

    def can_handle(self, message: str) -> bool:
        normalized_message = message.strip().lower()
        supported_questions = (
            "quanto gastei hoje",
            "quanto tenho em caixa",
            "qual categoria mais gastei",
            "quanto recebi esse mês",
        )
        return any(question in normalized_message for question in supported_questions)

    def summarize_capabilities(self) -> dict[str, list[str]]:
        return {
            "supported_examples": [
                "quanto tenho em caixa?",
                "quanto gastei hoje?",
                "qual categoria mais gastei?",
                "quanto recebi esse mês?",
            ],
            "status": ["available"],
        }

    def answer(self, user_id: int, question: str) -> str:
        normalized_question = question.strip().lower()

        if not normalized_question:
            raise ValueError("Digite uma pergunta para consultar o assistente financeiro.")

        if "quanto tenho em caixa" in normalized_question:
            balance = self.get_current_balance(user_id)
            return f"Seu saldo atual em caixa é de R$ {balance:.2f}."

        if "quanto gastei hoje" in normalized_question:
            total = self.get_today_expenses(user_id)
            return f"Hoje você gastou R$ {total:.2f}."

        if "qual categoria mais gastei" in normalized_question:
            category, total = self.get_top_expense_category(user_id)
            if not category:
                return "Ainda não há despesas suficientes para identificar uma categoria líder."
            return f"Sua categoria com maior despesa é '{category}' com R$ {total:.2f}."

        if "quanto recebi esse mês" in normalized_question:
            total = self.get_month_income(user_id)
            return f"Neste mês você recebeu R$ {total:.2f}."

        raise ValueError("Ainda não sei responder essa pergunta. Tente uma das sugestões do painel.")

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

    def get_today_expenses(self, user_id: int) -> float:
        today = date.today().isoformat()
        connection = get_db()
        row = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE user_id = ? AND type = 'expense' AND transaction_date = ?
            """,
            (user_id, today),
        ).fetchone()
        return float(row["total"])

    def get_top_expense_category(self, user_id: int) -> tuple[str | None, float]:
        connection = get_db()
        row = connection.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM transactions
            WHERE user_id = ? AND type = 'expense'
            GROUP BY category
            ORDER BY total DESC, category ASC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

        if row is None:
            return None, 0.0

        return str(row["category"]), float(row["total"])

    def get_month_income(self, user_id: int) -> float:
        month_prefix = date.today().strftime("%Y-%m")
        connection = get_db()
        row = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE user_id = ? AND type = 'income' AND transaction_date LIKE ?
            """,
            (user_id, f"{month_prefix}%"),
        ).fetchone()
        return float(row["total"])
