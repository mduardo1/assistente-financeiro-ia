from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.routes.auth import login_required
from app.services.dashboard_service import DashboardService
from app.services.financial_query_service import FinancialQueryService


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/")
@login_required
def index():
    summary = DashboardService().get_summary(session["user_id"])
    query_capabilities = FinancialQueryService().summarize_capabilities()
    query_answer = session.pop("financial_query_answer", None)
    query_value = session.pop("financial_query_value", "")
    return render_template(
        "dashboard/index.html",
        summary=summary,
        query_capabilities=query_capabilities,
        query_answer=query_answer,
        query_value=query_value,
    )


@dashboard_bp.post("/query")
@login_required
def query():
    question = request.form.get("question", "")
    service = FinancialQueryService()

    try:
        answer = service.answer(session["user_id"], question)
        flash("Consulta processada com sucesso.", "success")
    except ValueError as error:
        answer = str(error)
        flash("Não foi possível responder sua consulta.", "warning")

    session["financial_query_answer"] = answer
    session["financial_query_value"] = question
    return redirect(url_for("dashboard.index"))
