from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.routes.auth import login_required
from app.services.message_transaction_service import MessageTransactionService
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
    transaction_service = TransactionService()
    categories = transaction_service.list_categories(session["user_id"])

    try:
        saved = MessageTransactionService().parse_and_save(
            user_id=session["user_id"],
            message=request.form.get("message", ""),
            source="ai_parser",
        )
    except ValueError as error:
        transactions = transaction_service.list_transactions(session["user_id"])
        flash(str(error), "danger")
        return (
            render_template(
                "transactions/index.html",
                transactions=transactions,
                categories=categories,
                parser_form_data={"message": request.form.get("message", "")},
                filters={"type": "", "category": "", "date_start": "", "date_end": ""},
                today=date.today().isoformat(),
            ),
            400,
        )

    flash("Mensagem interpretada e movimentação salva com sucesso.", "success")
    return redirect(url_for("transactions.index"))


@transactions_bp.get("/simulador-whatsapp")
@login_required
def whatsapp_simulator():
    history = session.get("whatsapp_simulator_history", [])
    return render_template(
        "transactions/whatsapp_simulator.html",
        history=history,
    )


@transactions_bp.post("/simulador-whatsapp")
@login_required
def whatsapp_simulator_post():
    message = request.form.get("message", "")
    history = session.get("whatsapp_simulator_history", [])

    try:
        saved = MessageTransactionService().parse_and_save(
            user_id=session["user_id"],
            message=message,
            source="whatsapp_simulator",
        )
        reply = (
            f"✅ Movimentação salva: "
            f"{'entrada' if saved.parsed_data['type'] == 'income' else 'saída'} "
            f"de R$ {float(saved.parsed_data['amount']):.2f} em {saved.parsed_data['category']}."
        )
        flash("Mensagem simulada processada com sucesso.", "success")
    except ValueError as error:
        reply = str(error)
        flash("Não foi possível processar a mensagem simulada.", "danger")

    history.insert(
        0,
        {
            "message": message,
            "reply": reply,
        },
    )
    session["whatsapp_simulator_history"] = history[:8]
    return redirect(url_for("transactions.whatsapp_simulator"))
