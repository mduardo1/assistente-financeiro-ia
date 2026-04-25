from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.routes.auth import login_required
from app.services.openai_parser_service import OpenAIParserService
from app.services.transaction_service import TransactionService


transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions_bp.get("/")
@login_required
def index():
    service = TransactionService()
    filters = {
        "type": request.args.get("type", ""),
        "category": request.args.get("category", ""),
        "date_start": request.args.get("date_start", ""),
        "date_end": request.args.get("date_end", ""),
    }
    transactions = service.list_transactions(session["user_id"], filters=filters)
    categories = service.list_categories(session["user_id"])

    return render_template(
        "transactions/index.html",
        transactions=transactions,
        categories=categories,
        filters=filters,
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
        categories = service.list_categories(session["user_id"])
        return (
            render_template(
                "transactions/index.html",
                transactions=transactions,
                categories=categories,
                form_data=form_data,
                filters={"type": "", "category": "", "date_start": "", "date_end": ""},
                today=date.today().isoformat(),
            ),
            400,
        )

    flash(message, "success")
    return redirect(url_for("transactions.index"))


@transactions_bp.post("/parse")
@login_required
def create_from_message():
    parser_service = OpenAIParserService()
    transaction_service = TransactionService()
    message = request.form.get("message", "")

    try:
        parsed_data = parser_service.parse_message(message)
    except ValueError as error:
        flash(str(error), "danger")
        transactions = transaction_service.list_transactions(session["user_id"])
        categories = transaction_service.list_categories(session["user_id"])
        return (
            render_template(
                "transactions/index.html",
                transactions=transactions,
                categories=categories,
                parser_form_data={"message": message},
                filters={"type": "", "category": "", "date_start": "", "date_end": ""},
                today=date.today().isoformat(),
            ),
            400,
        )

    success, service_message = transaction_service.create_transaction(
        user_id=session["user_id"],
        form_data=parsed_data,
        source="ai_parser",
    )

    if not success:
        flash(service_message, "danger")
        transactions = transaction_service.list_transactions(session["user_id"])
        categories = transaction_service.list_categories(session["user_id"])
        return (
            render_template(
                "transactions/index.html",
                transactions=transactions,
                categories=categories,
                parser_form_data={"message": message},
                filters={"type": "", "category": "", "date_start": "", "date_end": ""},
                today=date.today().isoformat(),
            ),
            400,
        )

    flash("Mensagem interpretada e movimentação salva com sucesso.", "success")
    return redirect(url_for("transactions.index"))
