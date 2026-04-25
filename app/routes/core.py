from flask import Blueprint, redirect, render_template, session, url_for


core_bp = Blueprint("core", __name__)


@core_bp.get("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("core.home"))

    return redirect(url_for("auth.login"))


@core_bp.get("/home")
def home():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    return redirect(url_for("transactions.index"))
