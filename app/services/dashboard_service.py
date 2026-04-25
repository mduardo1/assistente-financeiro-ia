from app.database.connection import get_db


class DashboardService:
    def get_summary(self, user_id: int) -> dict[str, object]:
        connection = get_db()
        totals = connection.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) AS total_income,
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) AS total_expense,
                COUNT(*) AS transaction_count
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        categories = connection.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM transactions
            WHERE user_id = ? AND type = 'expense'
            GROUP BY category
            ORDER BY total DESC, category ASC
            """,
            (user_id,),
        ).fetchall()

        recent_transactions = connection.execute(
            """
            SELECT type, description, category, amount, transaction_date, source
            FROM transactions
            WHERE user_id = ?
            ORDER BY transaction_date DESC, id DESC
            LIMIT 5
            """,
            (user_id,),
        ).fetchall()

        biggest_expense = connection.execute(
            """
            SELECT description, amount
            FROM transactions
            WHERE user_id = ? AND type = 'expense'
            ORDER BY amount DESC, id DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

        biggest_income = connection.execute(
            """
            SELECT description, amount
            FROM transactions
            WHERE user_id = ? AND type = 'income'
            ORDER BY amount DESC, id DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

        top_expense_category = categories[0] if categories else None

        total_income = float(totals["total_income"])
        total_expense = float(totals["total_expense"])
        expenses_by_category = [
            {
                "category": row["category"],
                "total": float(row["total"]),
            }
            for row in categories
        ]

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense,
            "transaction_count": int(totals["transaction_count"]),
            "expenses_by_category": expenses_by_category,
            "recent_transactions": recent_transactions,
            "chart_data": {
                "labels": [item["category"].title() for item in expenses_by_category],
                "values": [item["total"] for item in expenses_by_category],
            },
            "income_vs_expense_chart": {
                "labels": ["Entradas", "Saídas"],
                "values": [total_income, total_expense],
            },
            "biggest_expense": None
            if biggest_expense is None
            else {
                "description": biggest_expense["description"],
                "amount": float(biggest_expense["amount"]),
            },
            "biggest_income": None
            if biggest_income is None
            else {
                "description": biggest_income["description"],
                "amount": float(biggest_income["amount"]),
            },
            "top_expense_category": None
            if top_expense_category is None
            else {
                "category": top_expense_category["category"],
                "amount": float(top_expense_category["total"]),
            },
        }
