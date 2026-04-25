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
        }
