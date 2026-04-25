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

    return redirect(url_for("dashboard.index"))


@core_bp.get("/sobre")
def about():
    return render_template("pages/about.html")


@core_bp.get("/como-funciona")
def how_it_works():
    return render_template("pages/how_it_works.html")


@core_bp.get("/proximos-recursos")
def next_features():
    return render_template("pages/next_features.html")
