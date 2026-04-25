from flask import Blueprint, render_template, session

from app.routes.auth import login_required
from app.services.dashboard_service import DashboardService


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/")
@login_required
def index():
    summary = DashboardService().get_summary(session["user_id"])
    return render_template("dashboard/index.html", summary=summary)
