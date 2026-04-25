from datetime import date

from flask import Blueprint, flash, render_template, request, session

from app.routes.auth import login_required
from app.services.transaction_service import TransactionService


transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions_bp.get("/")
@login_required
def index():
    service = TransactionService()
    transactions = service.list_transactions(session["user_id"])

    return render_template(
        "transactions/index.html",
        transactions=transactions,
        today=date.today().isoformat(),
    )


@transactions_bp.post("/")
@login_required
def create():
    service = TransactionService()
    form_data = {
        "type": request.form.get("type", ""),
        "description": request.form.get("description", ""),
        "category": request.form.get("category", ""),
        "amount": request.form.get("amount", ""),
        "transaction_date": request.form.get("transaction_date", ""),
    }
    success, message = service.create_transaction(
        user_id=session["user_id"],
        form_data=form_data,
    )

    if not success:
        flash(message, "danger")
        transactions = service.list_transactions(session["user_id"])
        return (
            render_template(
                "transactions/index.html",
                transactions=transactions,
                form_data=form_data,
                today=date.today().isoformat(),
            ),
            400,
        )

    flash(message, "success")
    transactions = service.list_transactions(session["user_id"])
    return render_template(
        "transactions/index.html",
        transactions=transactions,
        today=date.today().isoformat(),
    )
