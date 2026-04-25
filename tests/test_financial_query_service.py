from datetime import date

from app.database.connection import get_db
from app.services.financial_query_service import FinancialQueryService


def test_financial_query_current_balance(app):
    with app.app_context():
        connection = get_db()
        connection.execute(
            """
            INSERT INTO users (name, email, password_hash, whatsapp)
            VALUES ('Moyses', 'moyses@example.com', 'hash', NULL)
            """
        )
        connection.execute(
            """
            INSERT INTO transactions (user_id, type, description, category, amount, source, transaction_date)
            VALUES (1, 'income', 'Recebimento', 'cliente', 500, 'manual', ?)
            """,
            (date.today().isoformat(),),
        )
        connection.execute(
            """
            INSERT INTO transactions (user_id, type, description, category, amount, source, transaction_date)
            VALUES (1, 'expense', 'Mercado', 'mercado', 150, 'manual', ?)
            """,
            (date.today().isoformat(),),
        )
        connection.commit()

        answer = FinancialQueryService().answer(1, "quanto tenho em caixa?")

    assert "R$ 350.00" in answer


def test_financial_query_top_category(app):
    with app.app_context():
        connection = get_db()
        connection.execute(
            """
            INSERT INTO users (name, email, password_hash, whatsapp)
            VALUES ('Moyses', 'moyses@example.com', 'hash', NULL)
            """
        )
        connection.execute(
            """
            INSERT INTO transactions (user_id, type, description, category, amount, source, transaction_date)
            VALUES (1, 'expense', 'Mercado', 'mercado', 150, 'manual', ?)
            """,
            (date.today().isoformat(),),
        )
        connection.execute(
            """
            INSERT INTO transactions (user_id, type, description, category, amount, source, transaction_date)
            VALUES (1, 'expense', 'Internet', 'internet', 80, 'manual', ?)
            """,
            (date.today().isoformat(),),
        )
        connection.commit()

        answer = FinancialQueryService().answer(1, "qual categoria mais gastei?")

    assert "mercado" in answer
