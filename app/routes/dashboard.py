from flask import Blueprint, render_template, session

from app.routes.auth import login_required
from app.services.dashboard_service import DashboardService
from app.services.financial_query_service import FinancialQueryService


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/")
@login_required
def index():
    summary = DashboardService().get_summary(session["user_id"])
    query_capabilities = FinancialQueryService().summarize_capabilities()
    return render_template(
        "dashboard/index.html",
        summary=summary,
        query_capabilities=query_capabilities,
    )
